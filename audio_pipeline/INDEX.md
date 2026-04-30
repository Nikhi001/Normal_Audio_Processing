# Audio Processing Pipeline - Complete Index

## 📚 Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](README.md) | Comprehensive documentation, API reference, examples | All users |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute getting started guide | New users |
| [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md) | System design, extending the pipeline | Developers |
| [INDEX.md](INDEX.md) | This file - navigation guide | All users |

---

## 🚀 Getting Started

### For First-Time Users
1. Read: [QUICKSTART.md](QUICKSTART.md) (5 min)
2. Install: `pip install -r requirements.txt`
3. Run: `python main.py`
4. Follow the interactive menu

### For Developers
1. Read: [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md)
2. Study: [examples.py](examples.py)
3. Review: Source code in `processors/` and `utils/`

### For Advanced Usage
1. Read: [README.md](README.md) - Advanced Usage section
2. Modify: [config/settings.py](config/settings.py)
3. Extend: [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md) - Extending the Pipeline

---

## 📁 File Structure

### Root Level
```
audio_pipeline/
├── main.py                   # 👉 START HERE - Main entry point
├── examples.py               # Example code for all features
├── setup.py                  # Installation script
├── run.bat / run.sh          # Quick launch (Windows/Linux)
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── .gitignore               # Git ignore file
```

### Configuration
```
config/
├── __init__.py
└── settings.py              # ALL settings in one place
```

### Processors (Main Logic)
```
processors/
├── __init__.py
├── audio_converter.py       # MP3 → WAV conversion
├── bg_remover.py            # Background noise removal
├── duration_calculator.py   # Duration calculation
└── audio_filter.py          # Short file filtering
```

### Utilities (Helper Functions)
```
utils/
├── __init__.py
└── helpers.py               # Reusable utilities
    ├── CheckpointManager    # Save/load progress
    ├── FileScanner          # Find files
    ├── LoggerSetup          # Configure logging
    └── Helper functions     # Duration format, user input, etc.
```

### Generated at Runtime
```
logs/
├── pipeline.log             # Detailed operation log
└── checkpoint.json          # Resume information
```

---

## 🎯 What Each File Does

### [config/settings.py](config/settings.py)
**Contains:** All configuration in one place
**Edit for:** Changing defaults, enabling GPU, model paths
```python
AUDIO_CONVERSION_CONFIG = AudioConversionConfig()
BACKGROUND_REMOVAL_CONFIG = BackgroundRemovalConfig()
AUDIO_DURATION_CONFIG = AudioDurationConfig()
AUDIO_FILTER_CONFIG = AudioFilterConfig()
```

### [processors/audio_converter.py](processors/audio_converter.py)
**Class:** `AudioConverter`
**Methods:**
- `convert_file(input_path, output_path, format)` - Single file
- `convert_directory(input_dir, output_dir, ...)` - Batch convert
```python
converter = AudioConverter()
result = converter.convert_directory("in/", "out/", "mp3", "wav")
```

### [processors/bg_remover.py](processors/bg_remover.py)
**Class:** `BackgroundRemover`
**Methods:**
- `process_file(separator, input_path, ...)` - Single file
- `process_directory(input_dir, output_dir, model_file)` - Batch
```python
remover = BackgroundRemover()
result = remover.process_directory("in/", "out/", "model.ckpt")
```

### [processors/duration_calculator.py](processors/duration_calculator.py)
**Class:** `DurationCalculator`
**Methods:**
- `get_duration(filepath)` - Single file duration
- `calculate_directory_duration(folder)` - Total duration
- `calculate_multiple_directories(folders)` - Multiple folders
```python
calc = DurationCalculator()
result = calc.calculate_directory_duration("audio/")
print(result['formatted_duration'])
```

### [processors/audio_filter.py](processors/audio_filter.py)
**Class:** `AudioFilter`
**Methods:**
- `get_file_duration(filepath)` - Duration
- `is_valid_audio(filepath)` - Validation
- `filter_directory(folder, min_duration, dry_run)` - Filter
```python
filter_proc = AudioFilter()
result = filter_proc.filter_directory("audio/", 2.0, dry_run=True)
```

### [utils/helpers.py](utils/helpers.py)
**Classes:**
- `CheckpointManager` - Save/load processing progress
- `FileScanner` - Find and sort files
- `LoggerSetup` - Configure logging

**Functions:**
- `format_duration(seconds)` - Convert to readable format
- `get_user_input(prompt, is_path)` - Validated input
- `get_optional_input(prompt, default)` - With defaults

### [main.py](main.py)
**Class:** `AudioPipeline`
**Orchestrator:** Combines all processors
**Methods:**
- `run_conversion_step(...)` - Convert MP3→WAV
- `run_filter_step(...)` - Filter short files
- `run_background_removal_step(...)` - Remove background
- `run_duration_calculation_step(...)` - Calculate duration
- `run_full_pipeline(...)` - Run all steps
- `run_interactive()` - Interactive menu

### [examples.py](examples.py)
**Contains:** 7 complete examples
- Basic conversion
- Filtering short files
- Background removal
- Duration calculation
- Full pipeline
- Multiple folders
- Checkpoint recovery

---

## 🔄 Processing Workflows

### Workflow 1: Simple Conversion
```
MP3 File → Convert → WAV File
```
**Use:** `python main.py` → Select option 1

### Workflow 2: Convert & Calculate Duration
```
MP3s → Convert → WAVs → Calculate Duration
```
**Use:** Manual - run steps 1 then 4

### Workflow 3: Full Processing
```
MP3s → Convert → Filter → Remove BG → Calculate Duration
```
**Use:** `python main.py` → Select option 5

### Workflow 4: Programmatic
```python
pipeline = AudioPipeline()
pipeline.run_conversion_step("in/", "out/")
```

---

## 🛠️ Common Tasks

### Task: Convert MP3 to WAV
**Method 1:** Interactive
```bash
python main.py
# Select: 1
```

**Method 2:** Programmatic
```python
from processors.audio_converter import AudioConverter
converter = AudioConverter()
converter.convert_directory("mp3/", "wav/", "mp3", "wav")
```

**Method 3:** Direct
```bash
python -m audio_pipeline.processors.audio_converter
```

### Task: Check Audio Duration
**Method 1:** Interactive
```bash
python main.py
# Select: 4
```

**Method 2:** Programmatic
```python
from processors.duration_calculator import DurationCalculator
calc = DurationCalculator()
result = calc.calculate_directory_duration("audio/")
print(result['formatted_duration'])
```

### Task: Remove Short Files
**Method 1:** Interactive
```bash
python main.py
# Select: 2
```

**Method 2:** Programmatic
```python
from processors.audio_filter import AudioFilter
filter_proc = AudioFilter(min_duration=2.0)
filter_proc.filter_directory("audio/", min_duration=2.0, dry_run=False)
```

### Task: Full Pipeline
**Method 1:** Interactive
```bash
python main.py
# Select: 5
```

**Method 2:** Programmatic
```python
from main import AudioPipeline
pipeline = AudioPipeline()
pipeline.run_full_pipeline_interactive()
```

---

## 📊 Configuration Quick Reference

### To Enable GPU:
Edit `config/settings.py`:
```python
BACKGROUND_REMOVAL_CONFIG = BackgroundRemovalConfig(device="cuda")
```

### To Change Min Duration:
Edit `config/settings.py`:
```python
AUDIO_FILTER_CONFIG = AudioFilterConfig(min_duration_seconds=3.0)
```

### To Adjust Parallel Workers:
Edit `config/settings.py`:
```python
AUDIO_DURATION_CONFIG = AudioDurationConfig(max_workers=16)
```

### To Change Model:
Edit `config/settings.py`:
```python
BACKGROUND_REMOVAL_CONFIG = BackgroundRemovalConfig(
    model_name="your_model.ckpt"
)
```

---

## 🔍 Troubleshooting Guide

| Problem | Solution | File |
|---------|----------|------|
| GPU not detected | Check PyTorch install | [README.md](README.md#troubleshooting) |
| Missing dependencies | `pip install -r requirements.txt` | [requirements.txt](requirements.txt) |
| Permission denied | Check folder permissions | [README.md](README.md#troubleshooting) |
| No MP3 files found | Verify path and file format | [FileScanner in utils/helpers.py](utils/helpers.py) |
| Out of memory | Reduce batch size in config | [config/settings.py](config/settings.py) |

---

## 📖 Reading Guide

### 🟢 Start Here
1. [QUICKSTART.md](QUICKSTART.md) - 5 minutes
2. Run `python main.py` and explore

### 🟡 Next Level
1. [README.md](README.md) - 20 minutes
2. Review [examples.py](examples.py)
3. Try programmatic usage

### 🔴 Advanced
1. [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md)
2. Review source code in `processors/`
3. Extend with custom processors

---

## 🚀 Launch Options

### Option 1: Interactive Menu (Recommended)
```bash
python main.py
```
Shows menu with all options.

### Option 2: Direct Processor
```bash
python -m audio_pipeline.processors.audio_converter
```
Run specific processor directly.

### Option 3: Quick Launch Script
```bash
# Windows
run.bat

# Linux/Mac
./run.sh
```

### Option 4: Programmatic
```python
from audio_pipeline import AudioPipeline
pipeline = AudioPipeline()
pipeline.run_full_pipeline_interactive()
```

---

## 📞 Need Help?

1. Check relevant section in [README.md](README.md)
2. Review [QUICKSTART.md](QUICKSTART.md)
3. Look at [examples.py](examples.py)
4. Check logs: `logs/pipeline.log`
5. Review source code with inline comments

---

## ✅ Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Model file available (for background removal)
- [ ] Input folders exist and contain audio files
- [ ] Output folders have write permissions
- [ ] GPU/CUDA optional but recommended for speed
- [ ] Familiar with [QUICKSTART.md](QUICKSTART.md)
- [ ] Tested at least one processor

---

## 📦 Project Contents Summary

| Item | Count | Location |
|------|-------|----------|
| Processors | 4 | `processors/` |
| Config Classes | 6 | `config/settings.py` |
| Utility Classes | 3 | `utils/helpers.py` |
| Helper Functions | 6 | `utils/helpers.py` |
| Examples | 7 | `examples.py` |
| Documentation | 4 | `*.md` files |

---

## 🎯 Quick Navigation

- **Start Processing:** `python main.py`
- **Learn Basics:** [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation:** [README.md](README.md)
- **System Design:** [PIPELINE_ARCHITECTURE.md](PIPELINE_ARCHITECTURE.md)
- **Code Examples:** [examples.py](examples.py)
- **Configuration:** [config/settings.py](config/settings.py)
- **View Logs:** `logs/pipeline.log`

---

**Last Updated:** 2024  
**Version:** 1.0.0  
**Status:** Production Ready ✅
