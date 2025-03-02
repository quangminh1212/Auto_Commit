@echo off
echo Script de chay extension Auto Commit voi Copilot trong che do debug
echo.

rem Di chuyen den thu muc extension
cd extension

rem Bien dich TypeScript
echo Dang bien dich TypeScript...
call npm run compile

rem Chay extension trong che do debug
echo Dang chuan bi chay extension trong che do debug...
echo De chay extension trong che do debug:
echo 1. Mo thu muc extension trong VS Code
echo 2. Nhan F5 de bat dau phien debug
echo 3. Trong cua so VS Code moi, su dung phim tat Ctrl+Alt+C hoac menu ngu canh de chay lenh Auto Commit voi Copilot

rem Hoi nguoi dung co muon mo VS Code khong
set /p openVSCode=Ban co muon mo VS Code voi thu muc extension khong? (y/n): 
if "%openVSCode%"=="y" (
    echo Dang mo VS Code...
    code .
)

rem Tro ve thu muc goc
cd .. 