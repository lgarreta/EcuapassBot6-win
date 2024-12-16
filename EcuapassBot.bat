taskkill /IM "ecuapass_commander.exe" /F

echo "Actualizando EcuapassBot..."

git reset --hard 
git pull origin main

EcuapassBotGUI.exe
