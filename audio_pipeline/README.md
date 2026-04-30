# Audio Processing Pipeline

A modular and efficient Python pipeline for audio processing tasks including format conversion, background noise removal, duration calculation, and file filtering.

## 📋 Features

- **Audio Conversion**: Convert between multiple audio formats (MP3, WAV, FLAC, OGG, etc.)
- **Background Noise Removal**: Extract vocals using AI-powered audio separation
- **Duration Calculator**: Calculate total duration of audio files with parallel processing
- **Audio Filtering**: Remove short/invalid audio files based on duration threshold
- **Checkpoint System**: Resume interrupted processing sessions
- **Logging**: Comprehensive logging and error tracking
- **Progress Tracking**: Real-time progress bars with detailed status

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
cd c:\GitHub\Normal_Audio_Processing
```

2. Install dependencies:
```bash
pip install -r audio_pipeline/requirements.txt
```

For GPU support (CUDA), install PyTorch with CUDA:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Usage

#### Interactive Mode (Recommended)

```bash
cd audio_pipeline
python main.py
```

This opens an interactive menu where you can:
1. Convert MP3 to WAV
2. Filter short audio files
3. Remove background noise
4. Calculate audio duration
5. Run the full pipeline

#### Programmatic Usage

```python
from audio_pipeline import AudioPipeline

pipeline = AudioPipeline()

# Convert MP3 to WAV
result = pipeline.run_conversion_step(
    input_dir="path/to/mp3s",
    output_dir="path/to/wavs"
)

# Filter short files
pipeline.run_filter_step(
    input_dir="path/to/wavs",
    min_duration=2.0
)

# Remove background noise
pipeline.run_background_removal_step(
    input_dir="path/to/wavs",
    output_dir="path/to/clean/audio",
    model_file="model_bs_roformer_ep_317_sdr_12.9755.ckpt"
)

# Calculate duration
result = pipeline.run_duration_calculation_step("path/to/audio")
print(f"Total duration: {result['formatted_duration']}")
```

## 📁 Project Structure

```
audio_pipeline/
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration management
├── processors/
│   ├── __init__.py
│   ├── audio_converter.py       # MP3 to WAV conversion
│   ├── bg_remover.py            # Background noise removal
│   ├── duration_calculator.py   # Duration calculation
│   └── audio_filter.py          # Audio file filtering
├── utils/
│   ├── __init__.py
│   └── helpers.py               # Utility functions
├── logs/                         # Log files directory
├── main.py                       # Pipeline orchestrator
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## 🔧 Configuration

Edit `config/settings.py` to customize:

```python
# Audio conversion settings
AUDIO_CONVERSION_CONFIG = AudioConversionConfig(
    input_format="mp3",
    output_format="wav"
)

# Background removal settings
BACKGROUND_REMOVAL_CONFIG = BackgroundRemovalConfig(
    model_name="model_bs_roformer_ep_317_sdr_12.9755.ckpt",
    device="cuda"  # or "cpu"
)

# Duration calculation settings
AUDIO_DURATION_CONFIG = AudioDurationConfig(
    max_workers=8,
    include_subfolders=True
)

# Filtering settings
AUDIO_FILTER_CONFIG = AudioFilterConfig(
    min_duration_seconds=2.0
)
```

## 📊 Examples

### Convert Directory and Calculate Duration

```python
from audio_pipeline.processors import AudioConverter, DurationCalculator

converter = AudioConverter()
calculator = DurationCalculator()

# Convert all MP3s to WAV
converter.convert_directory(
    input_dir="/data/mp3_files",
    output_dir="/data/wav_files",
    input_format="mp3",
    output_format="wav"
)

# Calculate total duration
result = calculator.calculate_directory_duration("/data/wav_files")
print(f"Total duration: {result['formatted_duration']}")
print(f"Total files: {result['total_files']}")
```

### Filter and Remove Short Files

```python
from audio_pipeline.processors import AudioFilter

filter_proc = AudioFilter(min_duration=2.0)

# Dry run (preview what will be deleted)
result = filter_proc.filter_directory(
    folder="/data/audio_files",
    min_duration=2.0,
    dry_run=True
)

# Actually delete short files
result = filter_proc.filter_directory(
    folder="/data/audio_files",
    min_duration=2.0,
    dry_run=False
)
```

### Background Noise Removal

```python
from audio_pipeline.processors import BackgroundRemover

remover = BackgroundRemover()

result = remover.process_directory(
    input_dir="/data/noisy_audio",
    output_dir="/data/clean_audio",
    model_file="model_bs_roformer_ep_317_sdr_12.9755.ckpt"
)

print(f"Successfully processed: {result['success']} files")
print(f"Failed: {result['failed']} files")
print(f"Skipped: {result['skipped']} files")
```

## 🔌 Checkpoint System

The pipeline automatically saves checkpoints to resume interrupted processing:

```python
from audio_pipeline.utils import CheckpointManager

checkpoint_mgr = CheckpointManager("path/to/checkpoint.json")

# Load existing checkpoint
checkpoint = checkpoint_mgr.load()

# Mark file as processed
checkpoint_mgr.mark_processed(checkpoint, "file_path")

# Check if file was already processed
is_done = checkpoint_mgr.is_processed(checkpoint, "file_path")
```

## 📝 Logging

Logs are saved to `logs/pipeline.log` and also printed to console.

```python
from audio_pipeline.utils import LoggerSetup

logger = LoggerSetup.setup_logger(
    name="MyModule",
    log_file="logs/custom.log",
    level="DEBUG"
)

logger.info("Processing started")
logger.warning("Potential issue")
logger.error("An error occurred")
```

## ⚙️ Performance Tips

1. **GPU Acceleration**: Use CUDA for faster background noise removal
2. **Parallel Processing**: Duration calculator uses 8 workers by default
3. **Batch Processing**: Process entire directories at once
4. **Checkpoint Recovery**: Pipeline resumes from last successful file

## 🐛 Troubleshooting

### CUDA/GPU Issues
```bash
# Check PyTorch installation
python -c "import torch; print(torch.cuda.is_available())"

# Install CPU-only PyTorch if needed
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Missing Dependencies
```bash
pip install -r audio_pipeline/requirements.txt
```

### File Permission Errors
Ensure write permissions for output directories:
```bash
mkdir -p /path/to/output
chmod 755 /path/to/output
```

## 📋 Supported Audio Formats

- **Input**: MP3, M4A, OGG, FLAC, WAV, AIFF, AU, RF64
- **Output**: WAV (recommended), MP3, FLAC, OGG

## 🔍 Advanced Usage

### Run Full Pipeline

```bash
python main.py
# Then select option 5: "Run full pipeline"
```

### Process Multiple Directories

```python
from audio_pipeline.processors import DurationCalculator

calculator = DurationCalculator()

folders = [
    "/data/folder1",
    "/data/folder2",
    "/data/folder3"
]

result = calculator.calculate_multiple_directories(folders)
print(result['formatted_total'])
```

## 📚 API Reference

### AudioConverter
- `convert_file(input_path, output_path, format)`: Convert single file
- `convert_directory(input_dir, output_dir, input_format, output_format, recursive)`: Batch conversion

### BackgroundRemover
- `process_file(separator, input_path, filename, output_folder, checkpoint)`: Process single file
- `process_directory(input_dir, output_dir, model_file, recursive)`: Batch processing with checkpoints

### DurationCalculator
- `get_duration(filepath)`: Get duration of single file
- `calculate_directory_duration(folder, recursive)`: Calculate total duration
- `calculate_multiple_directories(folders)`: Process multiple directories

### AudioFilter
- `get_file_duration(filepath)`: Get file duration
- `is_valid_audio(filepath)`: Check if file is valid
- `filter_directory(folder, min_duration, recursive, dry_run)`: Filter files

## 📄 License

All rights reserved. For personal use only.

## 🤝 Contributing

Contributions are welcome! Please ensure code follows the existing style.

## 📞 Support

For issues or questions, check the logs in `logs/pipeline.log`

---

**Version**: 1.0.0  
**Last Updated**: 2024
