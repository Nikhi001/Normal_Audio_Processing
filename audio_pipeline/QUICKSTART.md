# Quick Start Guide - Audio Processing Pipeline

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd audio_pipeline
pip install -r requirements.txt
```

### Step 2: Run Interactive Pipeline
```bash
python main.py
```

### Step 3: Follow the Menu
```
AUDIO PROCESSING PIPELINE
==========================================
Select processing steps:
  1. Convert MP3 to WAV
  2. Filter short audio files
  3. Remove background noise (vocal extraction)
  4. Calculate audio duration
  5. Run full pipeline (1 -> 2 -> 3 -> 4)
  6. Exit
==========================================
```

---

## 📋 Common Tasks

### Convert MP3 to WAV
```bash
python main.py
# Select option: 1
# Enter input and output folders when prompted
```

### Calculate Audio Duration
```bash
python main.py
# Select option: 4
# Enter folder path
```

### Remove Background Noise
```bash
python main.py
# Select option: 3
# Enter input/output folders
# Ensure model file is available
```

### Run Full Pipeline
```bash
python main.py
# Select option: 5
# Follow prompts for each step
```

---

## 🐍 Python Usage

### In Your Script
```python
from audio_pipeline import AudioPipeline

pipeline = AudioPipeline()

# Convert MP3 to WAV
pipeline.run_conversion_step(
    input_dir="path/to/mp3s",
    output_dir="path/to/wavs"
)
```

### Individual Processors
```python
from audio_pipeline.processors import AudioConverter

converter = AudioConverter()
result = converter.convert_directory(
    input_dir="path/to/mp3s",
    output_dir="path/to/wavs",
    input_format="mp3",
    output_format="wav"
)
print(f"Success: {result['success']} / {result['total']}")
```

---

## 📁 File Structure
```
audio_pipeline/
├── config/              # Configuration files
├── processors/          # Processing modules
├── utils/               # Helper functions
├── logs/                # Log files
├── main.py              # Main entry point
├── examples.py          # Example scripts
├── README.md            # Full documentation
└── requirements.txt     # Dependencies
```

---

## ⚙️ Configuration

Edit `config/settings.py` to customize:
- Input/output formats
- GPU/CPU selection
- Model file location
- Logging settings
- Checkpoint location

---

## 🔍 Troubleshooting

**Issue**: GPU not detected
```bash
python -c "import torch; print(torch.cuda.is_available())"
# Install CPU version if False:
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Issue**: Missing dependencies
```bash
pip install -r requirements.txt
```

**Issue**: Permission denied on output folder
```bash
mkdir -p path/to/output
chmod 755 path/to/output
```

---

## 📊 Example Workflow

1. **Prepare Raw Files**
   - Put MP3 files in: `/Audio/raw_mp3`

2. **Convert to WAV**
   ```
   Select: 1
   Input: /Audio/raw_mp3
   Output: /Audio/converted_wav
   ```

3. **Filter Short Files**
   ```
   Select: 2
   Folder: /Audio/converted_wav
   Min duration: 2.0 seconds
   ```

4. **Remove Background Noise**
   ```
   Select: 3
   Input: /Audio/converted_wav
   Output: /Audio/clean_audio
   ```

5. **Check Duration**
   ```
   Select: 4
   Folder: /Audio/clean_audio
   ```

---

## 📝 Logging

All operations are logged to:
- Console (live output)
- `logs/pipeline.log` (file storage)

Check logs for detailed error messages and processing status.

---

## 🎯 Performance Tips

1. **Enable GPU** for faster background removal (3-5x faster)
2. **Batch process** entire directories at once
3. **Use checkpoints** to resume interrupted processing
4. **Increase parallel workers** in config for faster duration calculation

---

## 📚 Learn More

- See `README.md` for complete documentation
- See `examples.py` for code examples
- Check `logs/pipeline.log` for detailed logs

---

## 🆘 Need Help?

1. Check logs: `logs/pipeline.log`
2. Review examples: `examples.py`
3. Read full docs: `README.md`
4. Verify paths exist and have correct permissions
5. Ensure dependencies are installed: `pip install -r requirements.txt`

---

**Happy Processing! 🎉**
