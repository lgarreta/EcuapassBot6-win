@echo off
setlocal enabledelayedexpansion

:: File paths
set "LOG_FILE=patches.log"
set "CURRENT_FILE=..\ecuapass_commander\ecuapass_commander.exe"
set "ORIGINAL_FILE=..\ecuapass_commander\ecuapass_commander_original.exe"
set "NEW_FILE=..\ecuapass_commander\new_ecuapass_commander.exe"

cd /d "%~dp0"

:: Ensure log file exists
if not exist "%LOG_FILE%" type nul > "%LOG_FILE%"

:: Ensure original backup exists
if not exist "%ORIGINAL_FILE%" (
    echo +++ Creating original backup: %ORIGINAL_FILE%
    copy "%CURRENT_FILE%" "%ORIGINAL_FILE%" >nul || (
        echo !!! ERROR: Failed to create backup. Aborting.
        goto end
    )
)

:: Find the single patch file (e.g., patch_001.vcdiff)
set "PATCH_FILE="
for /f "delims=" %%F in ('dir /b patch_*.vcdiff 2^>nul') do set "PATCH_FILE=%%F"

if not defined PATCH_FILE (
    echo !!! No patch file found. Expected patch_*.vcdiff.
    goto end
)

:: Extract version using SPLIT (more reliable than string slicing)
for /f "tokens=2 delims=_" %%V in ("%PATCH_FILE%") do (
    for /f "tokens=1 delims=." %%N in ("%%V") do (
        set "PATCH_VERSION=%%N"
    )
)

if not defined PATCH_VERSION (
    echo !!! ERROR: Could not parse version from %PATCH_FILE%.
    goto end
)

:: Check if already applied
findstr /C:"%PATCH_VERSION%" "%LOG_FILE%" >nul && (
    echo +++ Patch %PATCH_VERSION% already applied. Skipping.
    goto end
)

echo +++ Applying patch %PATCH_FILE%...
xdelta3.exe -f -d -s "%ORIGINAL_FILE%" "%PATCH_FILE%" "%NEW_FILE%"

if not exist "%NEW_FILE%" (
    echo !!! ERROR: Patch failed--xdelta3 error--Aborting.
    goto end
)

echo +++ Update executable
del "%CURRENT_FILE%" && (
    move "%NEW_FILE%" "%CURRENT_FILE%" >nul || (
        echo !!! ERROR: Failed to replace EXE. Restore from backup if needed.
        goto end
    )
)

:: Prepend to log file (newest first)
echo %PATCH_VERSION% > temp.log
type "%LOG_FILE%" >> temp.log
move /y temp.log "%LOG_FILE%" >nul
echo +++ Successfully applied patch %PATCH_VERSION%.

:end
