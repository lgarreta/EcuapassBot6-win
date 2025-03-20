
::VERSION=0.001
::Applies to original executable all available patches in order (sorted by version).
::Prevents reapplying patches by checking patch.log.
::Stops on failure to avoid corrupting the executable.
::Ensures patches are always applied in sequence, even if a user was offline for a while.

@echo off
setlocal enabledelayedexpansion

:: Define file paths
set "LOG_FILE=patches.log"
set "CURRENT_FILE=..\ecuapass_commander\ecuapass_commander.exe"
set "ORIGINAL_FILE=..\ecuapass_commander\ecuapass_commander_original.exe"
set "NEW_FILE=..\ecuapass_commander\new_ecuapass_commander.exe"

echo ===================================
echo Checking for Updates from GitHub
echo ===================================

:: Change to the app directory
cd /d "%~dp0"

:: Ensure log file exists
if not exist "%LOG_FILE%" (
    echo +++ Creating log file: %LOG_FILE%
    type nul > "%LOG_FILE%"
)

:: Ensure the original backup exists
if not exist "%ORIGINAL_FILE%" (
    echo +++ Creating original file backup: %ORIGINAL_FILE%
    copy "%CURRENT_FILE%" "%ORIGINAL_FILE%" >nul
)

:: Loop through all patch files (sorted)
for /f "delims=" %%P in ('dir /b /o:n patch_*.vcdiff') do (
    set PATCH_FILE=%%P
    set PATCH_VERSION=%%~nP
    set PATCH_VERSION=!PATCH_VERSION:update_patch_=!

    echo +++ Checking Patch: !PATCH_FILE!

    :: Check if the patch is already applied
    findstr /C:"!PATCH_VERSION!" "%LOG_FILE%" >nul
    if !errorlevel! == 0 (
        echo +++ Patch !PATCH_VERSION! already applied. Skipping...
    ) else (
        echo +++ Applying patch !PATCH_VERSION!...
        xdelta3.exe -d -s "%ORIGINAL_FILE%" "!PATCH_FILE!" "%NEW_FILE%"

        if exist "%NEW_FILE%" (
            echo +++ Updating executable...
            del "%CURRENT_FILE%"
            move "%NEW_FILE%" "%CURRENT_FILE%"
            echo !PATCH_VERSION! >> "%LOG_FILE%"
        ) else (
            echo +++ Patch !PATCH_VERSION! failed! Stopping update process.
            goto end
        )
    )
)

:end
echo ===================================
echo Starting Java GUI...
echo ===================================

