@echo off
title CassSoft 95™ - Compilador do MACETADOR
color 1F
echo =============================
echo  Iniciando compilação...
echo =============================

:: Navegar até a pasta do script
cd /d "%~dp0"

:: Deleta build antigo (se tiver)
echo Limpando builds antigos...
rmdir /s /q build
rmdir /s /q dist
del /q *.spec

:: Compilar o novo EXE
echo Compilando Base.pyw...
python -m PyInstaller --noconfirm --windowed --onefile "Base.pyw"

:: Verifica se compilou
if exist "dist\Base.exe" (
    echo.
    echo =============================
    echo  Compilação feita com sucesso!
    echo  Movendo executável para a pasta correta...
    echo =============================

    move /Y "dist\Base.exe" "%~dp0\Base.exe" >nul

    echo.
    echo =========================================
    echo  MACETADOR atualizado com sucesso! 🔥
    echo  Executável salvo como Base.exe
    echo =========================================
) else (
    echo.
    echo =============================
    echo  ERRO: A compilação falhou :(
    echo =============================
)

pause
