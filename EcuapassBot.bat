
@echo off

REM Kill server if it still is running
taskkill /IM "ecuapass_commander.exe" /F 2>nul 

echo ========================================================
echo +++ Descargando Actualizaciones EcuapassBot...
echo ========================================================

REM Prevent Git from overwriting the patched executable
git update-index --assume-unchanged ecuapass_commander\ecuapass_commander.exe

REM Fetch and update repository while keeping user changes
git fetch origin main  && ^
git reset --keep origin/main && ^
git pull origin main

echo ========================================================
echo +++ Actualizando commander...
echo ========================================================
call patches\patch-update-exe-win.bat

echo ========================================================
echo +++ Ejecutando EcuapassBot...
echo ========================================================
EcuapassBotGUI.exe
pause
