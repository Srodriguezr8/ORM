:: filepath: c:\Users\johnp\OneDrive\Escritorio\tarea_ORMPOO\setup.bat
@echo off
echo Configurando entorno del proyecto Django...

:: Instalar dependencias Python
pip install -r requisitos.txt

:: Instalar dependencias Node.js para Tailwind
cd kj\static_src
npm install
npm run build

:: Volver al directorio raíz
cd ..\..

:: Configurar base de datos
echo Creando base de datos PostgreSQL 'biblioteca'...
:: Necesitarás tener psql de PostgreSQL en tu PATH
psql -U postgres -c "CREATE DATABASE biblioteca;"

:: Ejecutar migraciones
python manage.py migrate

echo ¡Configuración completa! Ejecuta 'python manage.py runserver' para iniciar el servidor de desarrollo.