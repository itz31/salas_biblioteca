@echo off
setlocal
cd /d "%~dp0"

if not exist "node_modules" (
	echo No se encontraron dependencias instaladas.
	choice /C YN /M "Deseas instalar las dependencias ahora?"
	if errorlevel 2 (
		echo.
		echo No se instalaron dependencias.
		echo Ejecuta npm install manualmente antes de usar este archivo.
		pause
		exit /b 1
	)
	echo Instalando dependencias del proyecto...
	call npm install
	if errorlevel 1 (
		echo.
		echo No se pudieron instalar las dependencias.
		echo Revisa tu conexion a internet y ejecuta npm install manualmente.
		pause
		exit /b 1
	)
)

start "Backend Salas Biblioteca" cmd /k "cd /d ""%~dp0"" && npm run dev"
timeout /t 5 /nobreak >nul
start "" "http://localhost:3000/index.html"
