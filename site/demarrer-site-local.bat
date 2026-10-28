@echo off
REM ============================================================
REM  ONEIRO PARIS - Apercu local du site
REM  Double-cliquez sur ce fichier : il lance un mini serveur web
REM  et ouvre le site dans votre navigateur.
REM  Pour arreter : fermez cette fenetre noire (ou Ctrl + C).
REM ============================================================
cd /d "%~dp0"
set PORT=8000

echo.
echo   ONEIRO - demarrage de l'apercu local...
echo.

REM --- Cherche Python, puis Node, puis PHP ---
where py >nul 2>&1
if %errorlevel%==0 (
    start "" "http://localhost:%PORT%/index.html"
    echo   Serveur actif sur http://localhost:%PORT%
    echo   Laissez cette fenetre ouverte pendant que vous consultez le site.
    echo.
    py -m http.server %PORT%
    goto :eof
)

where python >nul 2>&1
if %errorlevel%==0 (
    start "" "http://localhost:%PORT%/index.html"
    echo   Serveur actif sur http://localhost:%PORT%
    echo.
    python -m http.server %PORT%
    goto :eof
)

where npx >nul 2>&1
if %errorlevel%==0 (
    start "" "http://localhost:%PORT%/index.html"
    echo   Serveur actif sur http://localhost:%PORT%
    echo.
    npx --yes http-server -p %PORT% -c-1
    goto :eof
)

echo   [!] Ni Python ni Node n'ont ete trouves sur cet ordinateur.
echo.
echo   Installez Python (le plus simple) :
echo       https://www.python.org/downloads/
echo   Pensez a cocher "Add Python to PATH" pendant l'installation,
echo   puis relancez ce fichier.
echo.
pause
