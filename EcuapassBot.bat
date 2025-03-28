taskkill /IM "ecuapass_commander.exe" /F 2>nul 

@echo off
cd /d "%~dp0"  REM Ensure script runs in the repo directory

echo ========================================================
echo +++ Descargando Actualizaciones EcuapassBot...
echo ========================================================
REM Prevent Git from overwriting the patched executable
git update-index --assume-unchanged updates.bat ecuapass_commander\ecuapass_commander.exe

REM Fetch and update repository while keeping user changes
git fetch origin main  && ^
git reset --keep origin/main && ^
git pull origin main

echo ========================================================
echo +++ Realizando modificaciones...
echo ========================================================
call updates.bat

echo ========================================================
echo +++ Ejecutando EcuapassBot...
echo ========================================================
EcuapassBotGUI.exe
