@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=python"

echo Comprobando Python...
where %PYTHON% >nul 2>&1
if errorlevel 1 (
    echo No se encontro Python en la ruta, intentando py...
    where py >nul 2>&1
    if errorlevel 1 (
        echo No se encontro Python ni py en la ruta.
        echo Instala Python 3 y vuelve a intentarlo.
        pause
        exit /b 1
    )
    set "PYTHON=py"
)

for /f "usebackq tokens=2 delims= " %%V in (`%PYTHON% --version 2^>^&1`) do set "PY_VER=%%V"
for /f "tokens=1 delims=." %%A in ("%PY_VER%") do set "PY_MAJOR=%%A"
if "%PY_MAJOR%" LSS "3" (
    echo Se requiere Python 3 o superior. Se encontro: %PY_VER%
    pause
    exit /b 1
)

echo Usando %PYTHON% %PY_VER%

echo Verificando el entorno virtual...
if not exist "venv\Scripts\activate.bat" (
    echo No se encontro el entorno virtual "venv".
    echo Creando entorno virtual...
    %PYTHON% -m venv venv
    if errorlevel 1 (
        echo No se pudo crear el entorno virtual.
        echo Asegurate de tener permisos de escritura y Python instalado.
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo No se pudo activar el entorno virtual.
    pause
    exit /b 1
)

echo Instalando dependencias de Python...
%PYTHON% -m pip install --upgrade pip >nul 2>&1
%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 (
    echo Error al instalar las dependencias de Python.
    pause
    exit /b 1
)

echo Ejecutando migraciones de Django...
%PYTHON% manage.py migrate
if errorlevel 1 (
    echo Error al ejecutar manage.py migrate.
    pause
    exit /b 1
)

echo Iniciando servidor Django...
start "Servidor Django" cmd /k "cd /d "%~dp0" && call venv\Scripts\activate.bat && %PYTHON% manage.py runserver"
timeout /t 3 /nobreak >nul
start "" "http://localhost:8000"

endlocal
exit /b 0
