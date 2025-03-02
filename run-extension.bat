@echo off
echo Script de chay extension Auto Commit voi Copilot
echo.

rem Di chuyen den thu muc extension
cd extension

rem Bien dich TypeScript
echo Dang bien dich TypeScript...
call npm run compile

rem Dong goi extension
echo Dang dong goi extension...
call npx @vscode/vsce package

echo.
echo Huong dan cai dat:
echo 1. Mo VS Code
echo 2. Nhan F1 hoac Ctrl+Shift+P de mo Command Palette
echo 3. Go "Extensions: Install from VSIX" va chon file VSIX vua tao
echo 4. Sau khi cai dat, su dung phim tat Ctrl+Alt+C hoac menu ngu canh de chay lenh Auto Commit voi Copilot

rem Tro ve thu muc goc
cd .. 