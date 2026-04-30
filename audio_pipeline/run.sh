#!/bin/bash
# Audio Pipeline Launcher for Linux/Mac

echo ""
echo "=========================================
echo "    AUDIO PROCESSING PIPELINE LAUNCHER"
echo "========================================="
echo ""

if [ -z "$1" ]; then
    echo "Starting interactive mode..."
    python main.py
elif [ "$1" = "convert" ]; then
    python -m audio_pipeline.processors.audio_converter
elif [ "$1" = "filter" ]; then
    python -m audio_pipeline.processors.audio_filter
elif [ "$1" = "remove-bg" ]; then
    python -m audio_pipeline.processors.bg_remover
elif [ "$1" = "duration" ]; then
    python -m audio_pipeline.processors.duration_calculator
elif [ "$1" = "help" ]; then
    echo ""
    echo "Usage: ./run.sh [option]"
    echo ""
    echo "Options:"
    echo "  ./run.sh              - Start interactive mode"
    echo "  ./run.sh convert      - Run audio converter"
    echo "  ./run.sh filter       - Run audio filter"
    echo "  ./run.sh remove-bg    - Run background remover"
    echo "  ./run.sh duration     - Run duration calculator"
    echo "  ./run.sh help         - Show this help"
    echo ""
else
    echo "Unknown option: $1"
    echo "Use './run.sh help' for available options"
fi

read -p "Press enter to exit..."
