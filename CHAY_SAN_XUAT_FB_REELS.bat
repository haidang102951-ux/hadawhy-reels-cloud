@echo off
chcp 65001 >nul
echo =====================================================================
echo    ĐẦU NÃO SẢN XUẤT VIDEO NGẮN FB REELS - FORENSIC GLASS NOIR
echo =====================================================================
echo.
echo Cách dùng:
echo   python engine\render_reel.py --comp ^<TenComp^> --project "D:\DuAn_DangLam\^<ten_du_an^>" --name "^<TenVideo^>"
echo.
python "%~dp0engine\render_reel.py" --help
pause
