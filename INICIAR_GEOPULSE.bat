@echo off
title GeoPulse AI - Servidor Local
cd /d "c:\Users\mwfre\.gemini\antigravity\SEO IA sites"
echo ========================================================
echo   Iniciando o GeoPulse AI...
echo   Acesse no seu navegador: http://localhost:8000
echo ========================================================
start http://localhost:8000
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
