# FintechApp – Sistema Bancario Básico

Este proyecto simula el backend de una plataforma tipo Fintech, utilizando MySQL como sistema de base de datos. Permite registrar usuarios, crear cuentas bancarias, realizar transferencias entre cuentas y consultar el historial de movimientos.

## ¿Cómo instalar la base de datos?

Para instalar la base de datos, solo necesitas tener MySQL Workbench instalado. Luego, tiene que abrir la carpeta `BD_Examen_SQL` y ejecutar el primer script que es `login_app.sql`, en seguida de eso ejecutar el segundo script `datos_login_app.sql` y ya estaría instalado.

## Usuario de prueba

Puedes usar el siguiente usuario para probar la aplicación:

- **Usuario**: admin
- **Contraseña**: admin

## Ejemplos de operaciones

### Registrar un nuevo depósito en una cuenta:

1. En la pantalla de **"Cuenta"**, selecciona la opción **"Depositar"**.
2. Ingresa el monto que deseas depositar (por ejemplo, **100.00**).
3. Al confirmar, el sistema hará el depósito en la cuenta seleccionada.

**Ejemplo**: Depósito de 100.00 en la cuenta **Z9Y8X7W6V5U4T3S2**.

### Hacer una transferencia entre cuentas:

1. En la opción **"Transferir"**, ingresa el monto que deseas transferir (por ejemplo, **50.00**).
2. Selecciona la cuenta de **origen** y la cuenta de **destino**.
3. Confirma la operación.

**Ejemplo**: Transferencia de **50.00** desde la cuenta **606AA4B84DCEA72B** hacia la cuenta **2B81EA27CAEBC1F7**.

### Consultar el historial de movimientos de una cuenta:

1. Desde el menú principal, selecciona **"Consultar Movimientos"**.
2. La aplicación mostrará todas las operaciones realizadas en las cuentas asociadas, incluyendo depósitos, transferencias, etc.

## Integrantes del equipo

- **Hinojosa Torres Jose Reyes**
- **Luquin Lopez Carlos Alonso**

