taskkill /IM "ecuapass_server.exe" /F

echo "Actualizando EcuapassBot..."

git reset --hard 
git pull origin main

EcuapassBotGUI.exe
