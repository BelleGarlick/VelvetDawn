@echo off
title Velvet Dawn

set PYTHONPATH=src\server\src;%PYTHONPATH%

rem Scan for optional flags
FOR %%A IN (%*) DO (
    rem If /c is present...
    IF "%%A"=="/c" (
        rem ...drop all tables from the game database
        python src/server/src/velvet_dawn/dao/clean.py
    )
)

rem Scan for compulsory launch option
FOR %%A IN (%*) DO (
    IF "%%A"=="start" goto start
    IF "%%A"=="dev" goto dev
    IF "%%A"=="dev-fe" goto dev-fe
    IF "%%A"=="build" goto build
    IF "%%A"=="test-server" goto test-server
    IF "%%A"=="test" goto test
    IF "%%A"=="test-frontend" goto test-frontend
)

goto else

:start
rem Start the server in prod mode
py src\server\src\velvet_dawn\server\app.py
goto end

:dev
rem Start the server in dev mode
set DEV=true
python src/server/src/velvet_dawn/server/app.py
goto end

:dev-fe
rem Run the FE server for developing the front end
cd src/frontend
npx webpack serve
goto end

:build
rem Build the front end so the server runs it (maybe automate in github)
cd src/frontend
npm run magic
goto end

:test
rem Test all
python -m pytest
cd src/frontend
npm run test
goto end

:test-server
rem Test server
python -m pytest
goto end

:test-frontend
rem Test frontend
cd src/frontend
npm run test
goto end

:else
echo "Missing argument: start, dev, dev-fe, build, test, test-server, test-frontend"

:end
pause
