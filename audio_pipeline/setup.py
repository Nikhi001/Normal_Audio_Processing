#!/usr/bin/env python
"""
Setup script for Audio Processing Pipeline
"""

from setuptools import setup, find_packages
import os

# Get the directory where this script is located
setup_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(setup_dir, "..", "README.md")

with open(readme_path, "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="audio-pipeline",
    version="1.0.0",
    author="Audio Processing Team",
    description="Modular audio processing pipeline for conversion, filtering, and cleaning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydub>=0.25.1",
        "audio-separator>=0.17.0",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "soundfile>=0.12.1",
        "librosa>=0.10.0",
        "tqdm>=4.65.0",
        "numpy>=1.23.0",
        "scipy>=1.10.0",
    ],
    entry_points={
        "console_scripts": [
            "audio-pipeline=audio_pipeline.main:main",
            "audio-convert=audio_pipeline.processors.audio_converter:main",
            "audio-filter=audio_pipeline.processors.audio_filter:main",
            "audio-remove-bg=audio_pipeline.processors.bg_remover:main",
            "audio-duration=audio_pipeline.processors.duration_calculator:main",
        ],
    },
)
