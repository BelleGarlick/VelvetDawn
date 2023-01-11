@echo off

set PYTHONPATH=src\server\src;%PYTHONPATH%

if "%1"=="start" (
    rem Start the server in prod mode
    py src\server\src\velvet_dawn\server\app.py
) else (
    echo Missing argument: start
)

pause
