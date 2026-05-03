"""
Configuration settings for audio processing pipeline
"""

import os
from pathlib import Path
from dataclasses import dataclass

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent
PIPELINE_DIR = BASE_DIR / "audio_pipeline"
LOGS_DIR = PIPELINE_DIR / "logs"

# Ensure logs directory exists
LOGS_DIR.mkdir(exist_ok=True)


@dataclass
class AudioConversionConfig:
    """Configuration for MP3 to WAV conversion"""
    input_format: str = ".mp3"
    output_format: str = ".wav"
    supported_formats: tuple = (".mp3", ".m4a", ".ogg", ".flac")


@dataclass
class BackgroundRemovalConfig:
    """Configuration for background noise removal"""
    model_name: str = "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
    output_suffix: str = "_vocals"
    device: str = "cuda"  # or "cpu"
    batch_size: int = 1


@dataclass
class AudioDurationConfig:
    """Configuration for audio duration calculation"""
    supported_extensions: tuple = (".wav", ".mp3", ".flac", ".ogg", ".aiff", ".au")
    max_workers: int = 8
    include_subfolders: bool = True


@dataclass
class AudioFilterConfig:
    """Configuration for audio filtering"""
    min_duration_seconds: float = 2.0
    supported_extensions: tuple = (".wav", ".flac", ".ogg", ".aiff", ".au", ".rf64")


@dataclass
class CheckpointConfig:
    """Configuration for checkpoint management"""
    checkpoint_file: str = str(LOGS_DIR / "checkpoint.json")
    enable_checkpoints: bool = True


@dataclass
class LoggingConfig:
    """Configuration for logging"""
    log_dir: str = str(LOGS_DIR)
    log_file: str = str(LOGS_DIR / "pipeline.log")
    log_level: str = "INFO"
    enable_console_logging: bool = True
    enable_file_logging: bool = True


# Global configuration instances
AUDIO_CONVERSION_CONFIG = AudioConversionConfig()
BACKGROUND_REMOVAL_CONFIG = BackgroundRemovalConfig()
AUDIO_DURATION_CONFIG = AudioDurationConfig()
AUDIO_FILTER_CONFIG = AudioFilterConfig()
CHECKPOINT_CONFIG = CheckpointConfig()
LOGGING_CONFIG = LoggingConfig()
