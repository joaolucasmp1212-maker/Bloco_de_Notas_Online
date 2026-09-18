@echo off
cd /d "%~dp0"

:: Abre o navegador
start index.html

:: Inicia o Python mantendo a janela aberta (basta fechar o X dela para desligar)
python app.py
