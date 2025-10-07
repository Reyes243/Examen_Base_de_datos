USE LOGIN_APP;

DROP PROCEDURE IF EXISTS SP_TRANSFERIR_DINERO;
DROP PROCEDURE IF EXISTS SP_CONSULTAR_MOVIMIENTOS;
DROP PROCEDURE IF EXISTS SP_DEPOSITAR_DINERO;

DELIMITER $$

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