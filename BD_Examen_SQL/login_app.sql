CREATE DATABASE LOGIN_APP
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE LOGIN_APP;


CREATE TABLE users (
  id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL UNIQUE,
  password_hash CHAR(128) NOT NULL,
  firstname VARCHAR(255) NOT NULL,
  lastname VARCHAR(255) NOT NULL,
  password_salt CHAR(32) NOT NULL
) ENGINE=InnoDB;


DELIMITER $$
CREATE PROCEDURE SP_STORE_USER(
    IN v_username VARCHAR(50),
    IN v_password VARCHAR(255),
    IN v_firstname VARCHAR(100),
    IN v_lastname VARCHAR(100)
)
BEGIN
    DECLARE v_SALT CHAR(32);
    DECLARE v_PASSWORD_HASH CHAR(128);

    SET v_SALT = HEX(RANDOM_BYTES(16));
    SET v_PASSWORD_HASH = SHA2(CONCAT(v_password, v_SALT), 512);

    INSERT INTO users(username, password_hash, firstname, lastname, password_salt)
    VALUES (v_username, v_PASSWORD_HASH, v_firstname, v_lastname, v_SALT);
END$$
DELIMITER ;

-- Tabla de cuentas
CREATE TABLE accounts (
  id INT AUTO_INCREMENT PRIMARY KEY,
  account_number CHAR(16) NOT NULL UNIQUE,
  balance DECIMAL(10,2) DEFAULT 0.00,
  status ENUM('activa', 'bloqueada') DEFAULT 'activa',
  user_id INT NOT NULL,
  email VARCHAR(255) NOT NULL,
  firstname VARCHAR(255) NOT NULL,
  lastname VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;


DELIMITER $$

DROP PROCEDURE IF EXISTS SP_CREATE_ACCOUNT$$
CREATE PROCEDURE SP_CREATE_ACCOUNT(
    IN v_user_id INT,
    IN v_email VARCHAR(255),
    IN v_firstname VARCHAR(255),
    IN v_lastname VARCHAR(255)
)
BEGIN
    DECLARE v_account_number CHAR(16);

    -- Generar un número de cuenta único usando RANDOM_BYTES
    REPEAT
        SET v_account_number = UPPER(HEX(RANDOM_BYTES(8)));
    UNTIL NOT EXISTS (
        SELECT 1 FROM accounts WHERE account_number = v_account_number
    )
    END REPEAT;

    -- Insertar nueva cuenta
    INSERT INTO accounts (
        account_number, balance, status, user_id, email, firstname, lastname
    ) VALUES (
        v_account_number, 0.00, 'activa', v_user_id, v_email, v_firstname, v_lastname
    );
END$$
DELIMITER ;

-- Procedimiento de login
DELIMITER $$
CREATE PROCEDURE SP_LOGIN_USER(
    IN v_username VARCHAR(50),
    IN v_password VARCHAR(255)
)
BEGIN
    DECLARE v_salt CHAR(32);
    DECLARE v_hash CHAR(128);

    SELECT password_salt INTO v_salt FROM users WHERE username = v_username;

    IF v_salt IS NOT NULL THEN
        SET v_hash = SHA2(CONCAT(v_password, v_salt), 512);

        SELECT id, username, firstname, lastname
        FROM users
        WHERE username = v_username AND password_hash = v_hash;
    ELSE
        SELECT NULL AS id, NULL AS username, NULL AS firstname, NULL AS lastname;
    END IF;
END$$
DELIMITER ;

-- Tabla de movimientos (historial de operaciones)
CREATE TABLE movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_movimiento ENUM('APERTURA', 'TRANSFERENCIA_ENTRADA', 'TRANSFERENCIA_SALIDA') NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    cuenta_emisora CHAR(16),
    cuenta_receptora CHAR(16),
    fecha_operacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    nota TEXT,
    FOREIGN KEY (cuenta_emisora) REFERENCES accounts(account_number),
    FOREIGN KEY (cuenta_receptora) REFERENCES accounts(account_number),
    CHECK (monto > 0)
) ENGINE=InnoDB;

-- Procedimiento para transferir dinero entre cuentas
DELIMITER $$

DROP PROCEDURE IF EXISTS SP_TRANSFERIR_DINERO$$

CREATE PROCEDURE SP_TRANSFERIR_DINERO(
    IN v_cuenta_emisora CHAR(16),
    IN v_cuenta_receptora CHAR(16),
    IN v_monto DECIMAL(10,2),
    IN v_nota TEXT
)
BEGIN
    DECLARE v_saldo_emisor DECIMAL(10,2);
    DECLARE v_estado_emisor ENUM('activa', 'bloqueada');
    DECLARE v_estado_receptor ENUM('activa', 'bloqueada');
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    -- Validar que el monto sea positivo
    IF v_monto <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El monto debe ser positivo';
    END IF;

    -- Validar que no sea la misma cuenta
    IF v_cuenta_emisora = v_cuenta_receptora THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede transferir a la misma cuenta';
    END IF;

    -- Obtener saldo y estado de la cuenta emisora
    SELECT balance, status INTO v_saldo_emisor, v_estado_emisor 
    FROM accounts WHERE account_number = v_cuenta_emisora;

    -- Obtener estado de la cuenta receptora
    SELECT status INTO v_estado_receptor 
    FROM accounts WHERE account_number = v_cuenta_receptora;

    -- Validaciones
    IF v_saldo_emisor IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cuenta emisora no existe';
    END IF;

    IF v_estado_receptor IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cuenta receptora no existe';
    END IF;

    IF v_estado_emisor != 'activa' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cuenta emisora bloqueada';
    END IF;

    IF v_estado_receptor != 'activa' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cuenta receptora bloqueada';
    END IF;

    IF v_saldo_emisor < v_monto THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Saldo insuficiente';
    END IF;

    -- Iniciar transacción
    START TRANSACTION;

    -- Actualizar saldos
    UPDATE accounts SET balance = balance - v_monto 
    WHERE account_number = v_cuenta_emisora;

    UPDATE accounts SET balance = balance + v_monto 
    WHERE account_number = v_cuenta_receptora;

    -- Registrar movimiento de salida
    INSERT INTO movimientos (
        tipo_movimiento, monto, cuenta_emisora, cuenta_receptora, nota
    ) VALUES (
        'TRANSFERENCIA_SALIDA', v_monto, v_cuenta_emisora, v_cuenta_receptora, v_nota
    );

    -- Registrar movimiento de entrada
    INSERT INTO movimientos (
        tipo_movimiento, monto, cuenta_emisora, cuenta_receptora, nota
    ) VALUES (
        'TRANSFERENCIA_ENTRADA', v_monto, v_cuenta_emisora, v_cuenta_receptora, v_nota
    );

    -- Confirmar transacción
    COMMIT;
END$$

DELIMITER ;

-- Procedimiento para consultar movimientos de una cuenta
DELIMITER $$

DROP PROCEDURE IF EXISTS SP_CONSULTAR_MOVIMIENTOS$$

CREATE PROCEDURE SP_CONSULTAR_MOVIMIENTOS(
    IN v_cuenta_number CHAR(16)
)
BEGIN
    SELECT 
        m.tipo_movimiento,
        m.monto,
        m.cuenta_emisora,
        m.cuenta_receptora,
        m.fecha_operacion,
        m.nota
    FROM movimientos m
    WHERE m.cuenta_emisora = v_cuenta_number 
       OR m.cuenta_receptora = v_cuenta_number
    ORDER BY m.fecha_operacion DESC;
END$$

DELIMITER ;

-- Procedimiento para depositar dinero (apertura con saldo inicial)
DELIMITER $$

DROP PROCEDURE IF EXISTS SP_DEPOSITAR_DINERO$$

CREATE PROCEDURE SP_DEPOSITAR_DINERO(
    IN v_cuenta_number CHAR(16),
    IN v_monto DECIMAL(10,2),
    IN v_nota TEXT
)
BEGIN
    DECLARE v_estado ENUM('activa', 'bloqueada');
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    -- Validar que el monto sea positivo
    IF v_monto <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El monto debe ser positivo';
    END IF;

    -- Obtener estado de la cuenta
    SELECT status INTO v_estado FROM accounts WHERE account_number = v_cuenta_number;

    -- Validaciones
    IF v_estado IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cuenta no existe';
    END IF;

    IF v_estado != 'activa' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cuenta bloqueada';
    END IF;

    -- Iniciar transacción
    START TRANSACTION;

    -- Actualizar saldo
    UPDATE accounts SET balance = balance + v_monto 
    WHERE account_number = v_cuenta_number;

    -- Registrar movimiento
    INSERT INTO movimientos (
        tipo_movimiento, monto, cuenta_emisora, cuenta_receptora, nota
    ) VALUES (
        'APERTURA', v_monto, NULL, v_cuenta_number, v_nota
    );

    -- Confirmar transacción
    COMMIT;
END$$

DELIMITER ;

-- Datos de prueba
INSERT INTO users (username, password_hash, firstname, lastname, password_salt) VALUES
('admin', SHA2(CONCAT('admin', 'salt123'), 512), 'Admin', 'Sistema', 'salt123'),
('juan.perez', SHA2(CONCAT('password123', 'salt456'), 512), 'Juan', 'Pérez', 'salt456');

-- Insertar cuentas de prueba
INSERT INTO accounts (account_number, balance, status, user_id, email, firstname, lastname) VALUES
('A1B2C3D4E5F6G7H8', 1000.00, 'activa', 1, 'admin@fintech.com', 'Admin', 'Sistema'),
('Z9Y8X7W6V5U4T3S2', 500.00, 'activa', 2, 'juan@email.com', 'Juan', 'Pérez');

-- Insertar movimientos de prueba
INSERT INTO movimientos (tipo_movimiento, monto, cuenta_emisora, cuenta_receptora, nota) VALUES
('APERTURA', 1000.00, NULL, 'A1B2C3D4E5F6G7H8', 'Depósito inicial'),
('APERTURA', 500.00, NULL, 'Z9Y8X7W6V5U4T3S2', 'Depósito inicial');


SELECT * FROM users;
SELECT * FROM accounts;
select * FROM movimientos