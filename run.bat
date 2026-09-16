@echo off
echo 🎬 MovieFlix - Demarrage du serveur...
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installe
    pause
    exit /b 1
)

REM Installer les dependances si necessaire
echo Verification des dependances...
pip install -r requirements.txt

echo.
echo ✅ Demarrage du serveur Flask...
echo.
echo 🌍 Ouvrez votre navigateur a: http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

python app.py

pause
