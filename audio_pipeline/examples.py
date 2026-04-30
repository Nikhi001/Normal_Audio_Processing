"""
Example: Complete Audio Processing Workflow
Demonstrates how to use the audio pipeline
"""

def example_basic_conversion():
    """Example 1: Basic MP3 to WAV conversion"""
    from audio_pipeline.processors import AudioConverter
    
    converter = AudioConverter()
    
    result = converter.convert_directory(
        input_dir="C:/Audio/mp3_files",
        output_dir="C:/Audio/wav_files",
        input_format="mp3",
        output_format="wav",
        recursive=False
    )
    
    print(f"Conversion Results:")
    print(f"  Total: {result['total']}")
    print(f"  Success: {result['success']}")
    print(f"  Failed: {result['failed']}")


def example_filter_short_files():
    """Example 2: Filter out short audio files"""
    from audio_pipeline.processors import AudioFilter
    
    filter_processor = AudioFilter(min_duration=2.0)
    
    # Dry run - just show what will be deleted
    result = filter_processor.filter_directory(
        folder="C:/Audio/wav_files",
        min_duration=2.0,
        recursive=True,
        dry_run=True
    )
    
    print(f"\nFiles to be filtered:")
    print(f"  Short files: {len(result['short_files'])}")
    print(f"  Invalid files: {len(result['invalid_files'])}")


def example_background_removal():
    """Example 3: Remove background noise"""
    from audio_pipeline.processors import BackgroundRemover
    
    remover = BackgroundRemover()
    
    result = remover.process_directory(
        input_dir="C:/Audio/clean_wav_files",
        output_dir="C:/Audio/vocal_only",
        model_file="model_bs_roformer_ep_317_sdr_12.9755.ckpt",
        recursive=False
    )
    
    print(f"\nBackground Removal Results:")
    print(f"  Total: {result['total']}")
    print(f"  Success: {result['success']}")
    print(f"  Skipped: {result['skipped']}")
    print(f"  Failed: {result['failed']}")


def example_duration_calculation():
    """Example 4: Calculate audio duration"""
    from audio_pipeline.processors import DurationCalculator
    
    calculator = DurationCalculator()
    
    result = calculator.calculate_directory_duration(
        folder="C:/Audio/vocal_only",
        recursive=True
    )
    
    print(f"\nAudio Duration:")
    print(f"  Total files: {result['total_files']}")
    print(f"  Total duration: {result['formatted_duration']}")
    print(f"  Average per file: {result['average_duration']:.2f} seconds")


def example_full_pipeline():
    """Example 5: Run the complete pipeline"""
    from audio_pipeline import AudioPipeline
    
    pipeline = AudioPipeline()
    
    print("\n" + "="*60)
    print("RUNNING FULL AUDIO PROCESSING PIPELINE")
    print("="*60)
    
    # Step 1: Convert MP3 to WAV
    print("\n[STEP 1] Converting MP3 to WAV...")
    conv_result = pipeline.run_conversion_step(
        input_dir="C:/Audio/raw_mp3",
        output_dir="C:/Audio/step1_converted",
        input_format="mp3",
        output_format="wav"
    )
    print(f"✓ Converted: {conv_result['success']} files\n")
    
    # Step 2: Filter short files
    print("[STEP 2] Filtering short files...")
    pipeline.run_filter_step(
        input_dir="C:/Audio/step1_converted",
        min_duration=2.0
    )
    print("✓ Filtering complete\n")
    
    # Step 3: Remove background noise
    print("[STEP 3] Removing background noise...")
    removal_result = pipeline.run_background_removal_step(
        input_dir="C:/Audio/step1_converted",
        output_dir="C:/Audio/step3_cleaned",
        model_file="model_bs_roformer_ep_317_sdr_12.9755.ckpt"
    )
    print(f"✓ Cleaned: {removal_result['success']} files\n")
    
    # Step 4: Calculate duration
    print("[STEP 4] Calculating audio duration...")
    duration_result = pipeline.run_duration_calculation_step(
        input_dir="C:/Audio/step3_cleaned"
    )
    print(f"✓ Total duration: {duration_result['formatted_duration']}\n")
    
    print("="*60)
    print("PIPELINE COMPLETE!")
    print("="*60)
    print(f"Output directory: C:/Audio/step3_cleaned")
    print(f"Total processed: {removal_result['total']} files")
    print(f"Final duration: {duration_result['formatted_duration']}")


def example_multiple_folders():
    """Example 6: Process multiple directories"""
    from audio_pipeline.processors import DurationCalculator
    
    calculator = DurationCalculator()
    
    folders = [
        "C:/Audio/dataset1",
        "C:/Audio/dataset2",
        "C:/Audio/dataset3"
    ]
    
    result = calculator.calculate_multiple_directories(folders)
    
    print(f"\nMultiple Folder Summary:")
    print(f"  Grand total files: {result['grand_total_files']}")
    print(f"  Grand total duration: {result['formatted_total']}")


def example_checkpoint_recovery():
    """Example 7: Resume from checkpoint"""
    from audio_pipeline.utils import CheckpointManager
    from audio_pipeline.processors import BackgroundRemover
    
    # Load existing checkpoint or create new one
    checkpoint_mgr = CheckpointManager("C:/Audio/logs/checkpoint.json")
    checkpoint = checkpoint_mgr.load()
    
    print(f"Checkpoint loaded:")
    print(f"  Already processed: {len(checkpoint.get('processed_files', []))} files")
    print(f"  Failed files: {len(checkpoint.get('failed_files', {}))} files")
    
    # Continue processing from where we left off
    remover = BackgroundRemover()
    
    result = remover.process_directory(
        input_dir="C:/Audio/wav_files",
        output_dir="C:/Audio/cleaned",
        model_file="model_bs_roformer_ep_317_sdr_12.9755.ckpt"
    )
    
    print(f"\nProcessing resumed and completed:")
    print(f"  New successful: {result['success']} files")
    print(f"  Skipped (already done): {result['skipped']} files")


if __name__ == "__main__":
    print("""
    Audio Pipeline Examples
    =======================
    
    Uncomment the example you want to run:
    """)
    
    # Uncomment the example you want to run:
    
    # example_basic_conversion()
    # example_filter_short_files()
    # example_background_removal()
    # example_duration_calculation()
    # example_full_pipeline()
    # example_multiple_folders()
    # example_checkpoint_recovery()
    
    print("\nRun the examples by uncommenting them in this file")
    print("Or use: python -m audio_pipeline.main")
