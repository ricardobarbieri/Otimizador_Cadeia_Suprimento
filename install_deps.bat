@echo off
echo Verificando e instalando dependencias...

REM Define o caminho para o Python (ajuste se necessário)
set PYTHON=python

REM Verifica se o pip está instalado
%PYTHON% -m pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Erro: pip nao encontrado. Certifique-se de que o Python esta instalado e configurado no PATH.
    pause
    exit /b 1
)

REM Verifica e instala as dependencias listadas no requirements.txt
echo Instalando bibliotecas do requirements.txt...
%PYTHON% -m pip install -r requirements.txt

REM Verifica se a instalacao foi bem-sucedida
if %ERRORLEVEL% EQU 0 (
    echo Todas as dependencias foram instaladas com sucesso!
) else (
    echo Erro ao instalar dependencias. Verifique sua conexao ou permissoes.
)

REM Pausa para o usuario ver o resultado
pause