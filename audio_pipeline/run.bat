@echo off
REM Audio Pipeline Launcher for Windows

setlocal enabledelayedexpansion

cls
echo.
echo =========================================
echo    AUDIO PROCESSING PIPELINE LAUNCHER
echo =========================================
echo.

if "%1"=="" (
    echo Starting interactive mode...
    python main.py
) else if "%1"=="convert" (
    python -m audio_pipeline.processors.audio_converter
) else if "%1"=="filter" (
    python -m audio_pipeline.processors.audio_filter
) else if "%1"=="remove-bg" (
    python -m audio_pipeline.processors.bg_remover
) else if "%1"=="duration" (
    python -m audio_pipeline.processors.duration_calculator
) else if "%1"=="help" (
    echo.
    echo Usage: run.bat [option]
    echo.
    echo Options:
    echo   run.bat              - Start interactive mode
    echo   run.bat convert      - Run audio converter
    echo   run.bat filter       - Run audio filter
    echo   run.bat remove-bg    - Run background remover
    echo   run.bat duration     - Run duration calculator
    echo   run.bat help         - Show this help
    echo.
) else (
    echo Unknown option: %1
    echo Use "run.bat help" for available options
)

pause
