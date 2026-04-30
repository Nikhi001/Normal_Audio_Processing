# Audio Pipeline Architecture

## 🏗️ System Design Overview

The Audio Processing Pipeline is built using a modular, extensible architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                    AudioPipeline (main.py)                  │
│                 - Orchestrates processing steps              │
│                 - Provides interactive menu                  │
│                 - Manages workflow                           │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │             │             │
        ┌───────▼──────┐ ┌──▼─────────┐ ┌─▼──────────┐
        │ Processors   │ │  Config    │ │  Utils     │
        └─────────────┘ └────────────┘ └────────────┘
         │  │  │  │      (settings)    (helpers)
         │  │  │  │
    ┌────┘  │  │  └─────┐
    │       │  │        │
  Conv    Filter BG    Duration
        Remover    Calc
```

## 📁 Directory Structure

```
audio_pipeline/
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration dataclasses
│
├── processors/               # Individual processing modules
│   ├── __init__.py
│   ├── audio_converter.py    # AudioConverter class
│   ├── bg_remover.py         # BackgroundRemover class
│   ├── duration_calculator.py # DurationCalculator class
│   └── audio_filter.py       # AudioFilter class
│
├── utils/
│   ├── __init__.py
│   └── helpers.py            # Utility classes and functions
│
├── logs/                     # Runtime logs (created)
│   ├── pipeline.log
│   └── checkpoint.json
│
├── main.py                   # AudioPipeline orchestrator
├── examples.py               # Usage examples
├── setup.py                  # Installation script
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── run.bat / run.sh          # Quick launch scripts
├── README.md                 # Full documentation
├── QUICKSTART.md             # Quick start guide
└── PIPELINE_ARCHITECTURE.md  # This file
```

## 🔄 Data Flow

### Audio Conversion Pipeline
```
[Input MP3 Files]
        │
        ▼
[AudioConverter.convert_file()]
        │
        ├─→ Load audio with pydub
        ├─→ Create output directory
        ├─→ Export to target format
        │
        ▼
[Output WAV Files]
```

### Background Removal Pipeline
```
[Input WAV Files]
        │
        ▼
[CheckpointManager.load()]  ◄─ Recover from interruptions
        │
        ├─ Skip already processed
        │
        ▼
[BackgroundRemover.process_file()]
        │
        ├─→ Load audio-separator model
        ├─→ Separate vocals from background
        ├─→ Move output files
        ├─→ Clean up temporary files
        │
        ▼
[CheckpointManager.mark_processed()]  ◄─ Save progress
        │
        ▼
[Output Vocals-Only Files]
```

### Duration Calculation Pipeline
```
[Input Audio Directory]
        │
        ▼
[FileScanner.find_files()]  ◄─ Scan for audio files
        │
        ▼
[ThreadPoolExecutor]  ◄─ Parallel processing
        │
        ├─→ [DurationCalculator.get_duration()] x N
        │
        ▼
[Aggregate Results]
        │
        ▼
[Print Summary & Statistics]
```

## 🔌 Key Components

### 1. Configuration (config/settings.py)

Dataclass-based configuration for centralized settings:

```python
@dataclass
class AudioConversionConfig:
    input_format: str = "mp3"
    output_format: str = "wav"
    
# Usage
from config.settings import AUDIO_CONVERSION_CONFIG
format_out = AUDIO_CONVERSION_CONFIG.output_format
```

**Benefits:**
- Type-safe configuration
- Easy to extend
- Single source of truth
- Default values

### 2. Utility Layer (utils/helpers.py)

Reusable helper classes:

#### CheckpointManager
- Saves/loads checkpoint JSON
- Tracks processed files
- Enables resumable processing
- Error tracking

#### FileScanner
- Finds files by extension
- Sorts numerically
- Maintains directory structure
- Recursive or flat scanning

#### LoggerSetup
- Centralized logging configuration
- Console and file output
- Consistent formatting
- Different log levels

### 3. Processor Classes

Each processor is independent but follows the same pattern:

```python
class BaseProcessor:
    def __init__(self):
        self.config = CONFIG_INSTANCE
        self.logger = LoggerSetup.setup_logger("ProcessorName")
    
    def process_file(self, input_path, **kwargs):
        """Process single item"""
        try:
            # Main logic
            self.logger.info("Success")
            return True
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return False
    
    def process_directory(self, input_dir, output_dir, **kwargs):
        """Process all items in directory"""
        files = FileScanner.find_files(input_dir, extensions)
        
        with tqdm(files) as pbar:
            for file in pbar:
                self.process_file(file, **kwargs)
                pbar.update(1)
```

### 4. Pipeline Orchestrator (main.py)

Coordinates multiple processors:

```python
class AudioPipeline:
    def __init__(self):
        self.converter = AudioConverter()
        self.remover = BackgroundRemover()
        self.calculator = DurationCalculator()
    
    def run_conversion_step(self, input_dir, output_dir):
        return self.converter.convert_directory(...)
    
    def run_full_pipeline(self):
        # Chain multiple steps
```

## 🎯 Design Patterns

### 1. Strategy Pattern (Processors)
Each processor implements a specific strategy for audio processing.

### 2. Factory Pattern (LoggerSetup)
Creates and configures loggers centrally.

### 3. Singleton-like Pattern (Configuration)
Global config instances available throughout the app.

### 4. Command Pattern (Interactive Menu)
Menu items map to processor operations.

### 5. Chain of Responsibility (Full Pipeline)
Steps execute in sequence, passing output as input.

## 🔧 Extending the Pipeline

### Add a New Processor

1. **Create new file** `processors/my_processor.py`:

```python
from ..config.settings import MY_PROCESSOR_CONFIG
from ..utils.helpers import FileScanner, LoggerSetup

class MyProcessor:
    def __init__(self):
        self.config = MY_PROCESSOR_CONFIG
        self.logger = LoggerSetup.setup_logger("MyProcessor")
    
    def process_file(self, input_path):
        # Your logic here
        pass
    
    def process_directory(self, input_dir, output_dir):
        files = FileScanner.find_files(input_dir, extensions)
        # Process all files
        pass
```

2. **Add config** to `config/settings.py`:

```python
@dataclass
class MyProcessorConfig:
    param1: str = "default"
    param2: int = 10

MY_PROCESSOR_CONFIG = MyProcessorConfig()
```

3. **Update** `processors/__init__.py`:

```python
from .my_processor import MyProcessor
__all__ = [..., "MyProcessor"]
```

4. **Integrate into pipeline** `main.py`:

```python
class AudioPipeline:
    def __init__(self):
        self.my_processor = MyProcessor()
    
    def run_my_step(self, ...):
        return self.my_processor.process_directory(...)
```

### Add New Configuration

1. Create dataclass in `config/settings.py`
2. Instantiate at module level
3. Import in processors: `from ..config.settings import MY_CONFIG`

### Custom Logging

```python
from utils.helpers import LoggerSetup

logger = LoggerSetup.setup_logger(
    "MyModule",
    log_file="logs/custom.log",
    level="DEBUG"
)
```

## 📊 Error Handling

### Checkpoint-Based Recovery

```python
checkpoint = CheckpointManager.load()

# Skip already processed
if CheckpointManager.is_processed(checkpoint, filepath):
    continue

# Process
try:
    # Main logic
    CheckpointManager.mark_processed(checkpoint, filepath)
except Exception as e:
    CheckpointManager.mark_failed(checkpoint, filepath, str(e))
```

### Logging

All errors are:
1. Logged to `logs/pipeline.log`
2. Printed to console
3. Tracked in tqdm progress bar

## ⚙️ Performance Considerations

### Parallel Processing
- Duration calculator uses ThreadPoolExecutor
- Configurable worker count
- Non-blocking I/O operations

### Memory Management
- Process files one at a time
- Stream large audio files
- Automatic cleanup of temporary files

### GPU Acceleration
- Optional CUDA support for background removal
- Automatic CPU fallback
- Configurable device selection

## 🧪 Testing Strategy

### Unit Testing
Test individual processors independently:

```python
def test_audio_converter():
    converter = AudioConverter()
    result = converter.convert_file("input.mp3", "output.wav")
    assert result == True
```

### Integration Testing
Test full pipeline:

```python
def test_full_pipeline():
    pipeline = AudioPipeline()
    result = pipeline.run_full_pipeline(...)
    assert result['success'] > 0
```

## 📈 Scalability

### Handle Large Datasets
1. Use recursive directory scanning
2. Process in batches
3. Leverage parallel workers
4. Save checkpoints frequently

### Memory Optimization
1. Stream files instead of loading fully
2. Delete temporary files
3. Use appropriate data structures

## 🔐 Best Practices

1. **Always use checkpoints** for long-running operations
2. **Validate inputs** before processing
3. **Log everything** for debugging
4. **Handle exceptions** gracefully
5. **Clean up resources** (temp files, models)
6. **Use type hints** for clarity
7. **Follow DRY principle** - reuse utilities
8. **Document code** with docstrings

## 📚 Learning Resources

- See `examples.py` for usage patterns
- See `README.md` for API documentation
- Check `QUICKSTART.md` for beginner guide
- Review individual processor files for implementation details

## 🚀 Future Enhancements

- [ ] Web UI for pipeline management
- [ ] REST API for remote processing
- [ ] Distributed processing across multiple machines
- [ ] Real-time progress streaming
- [ ] Advanced audio analysis (noise profile, voice detection)
- [ ] Batch scheduling
- [ ] Performance profiling
- [ ] Pipeline versioning

---

**Architecture Version**: 1.0  
**Last Updated**: 2024
