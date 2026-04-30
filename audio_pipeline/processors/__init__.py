"""
Audio processors module
"""

from .audio_converter import AudioConverter
from .bg_remover import BackgroundRemover
from .duration_calculator import DurationCalculator
from .audio_filter import AudioFilter

__all__ = [
    "AudioConverter",
    "BackgroundRemover",
    "DurationCalculator",
    "AudioFilter"
]
