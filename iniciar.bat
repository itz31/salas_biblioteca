@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
	echo No se encontro el entorno virtual.
	echo Creando .venv con Python del sistema...
	python -m venv .venv
	if errorlevel 1 (
		echo No se pudo crear el entorno virtual.
		pause
		exit /b 1
	)
)

echo Instalando dependencias de Django si hace falta...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 (
	echo No se pudieron instalar las dependencias.
	pause
	exit /b 1
)

echo Aplicando migraciones...
"%PYTHON%" manage.py migrate
if errorlevel 1 (
	echo Fallo la migracion de la base de datos.
	pause
	exit /b 1
)

echo Cargando datos iniciales desde los JSON existentes...
"%PYTHON%" manage.py import_json_data

echo Iniciando servidor Django...
start "Servidor Django" cmd /k "cd /d ""%~dp0"" && .venv\Scripts\python.exe manage.py runserver"
timeout /t 4 /nobreak >nul
start "" "http://127.0.0.1:8000"
