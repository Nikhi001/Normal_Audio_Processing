"""
Main pipeline orchestrator - Combine and run multiple processing steps
"""

import os
import logging
from typing import Dict, Any
from pathlib import Path

from .processors.audio_converter import AudioConverter
from .processors.bg_remover import BackgroundRemover
from .processors.duration_calculator import DurationCalculator
from .processors.audio_filter import AudioFilter
from .utils.helpers import LoggerSetup, get_optional_input


class AudioPipeline:
    """Main pipeline orchestrator"""
    
    def __init__(self):
        self.logger = LoggerSetup.setup_logger("AudioPipeline")
        self.converter = AudioConverter()
        self.remover = BackgroundRemover()
        self.duration_calc = DurationCalculator()
        self.filter_proc = AudioFilter()
    
    def run_conversion_step(self, input_dir: str, output_dir: str, 
                           input_format: str = "mp3", output_format: str = "wav") -> Dict[str, Any]:
        """Run audio conversion step"""
        self.logger.info(f"Running conversion: {input_format} -> {output_format}")
        print(f"\n{'='*60}")
        print("STEP 1: AUDIO CONVERSION")
        print(f"{'='*60}")
        
        result = self.converter.convert_directory(input_dir, output_dir, input_format, output_format)
        return result
    
    def run_filter_step(self, input_dir: str, min_duration: float = 2.0) -> Dict[str, Any]:
        """Run audio filter step"""
        self.logger.info(f"Running filter: removing files < {min_duration}s")
        print(f"\n{'='*60}")
        print("STEP 2: AUDIO FILTERING")
        print(f"{'='*60}")
        
        result = self.filter_proc.filter_directory(input_dir, min_duration, dry_run=False)
        return result
    
    def run_background_removal_step(self, input_dir: str, output_dir: str, 
                                   model_file: str) -> Dict[str, Any]:
        """Run background removal step"""
        self.logger.info("Running background removal")
        print(f"\n{'='*60}")
        print("STEP 3: BACKGROUND NOISE REMOVAL")
        print(f"{'='*60}")
        
        result = self.remover.process_directory(input_dir, output_dir, model_file)
        return result
    
    def run_duration_calculation_step(self, input_dir: str) -> Dict[str, Any]:
        """Run duration calculation step"""
        self.logger.info("Running duration calculation")
        print(f"\n{'='*60}")
        print("STEP 4: DURATION CALCULATION")
        print(f"{'='*60}")
        
        result = self.duration_calc.calculate_directory_duration(input_dir)
        return result
    
    def print_pipeline_menu(self):
        """Display main pipeline menu"""
        print("\n" + "=" * 60)
        print("AUDIO PROCESSING PIPELINE")
        print("=" * 60)
        print("\nSelect processing steps:")
        print("  1. Convert MP3 to WAV")
        print("  2. Filter short audio files")
        print("  3. Remove background noise (vocal extraction)")
        print("  4. Calculate audio duration")
        print("  5. Run full pipeline (1 -> 2 -> 3 -> 4)")
        print("  6. Exit")
        print("=" * 60)
    
    def run_interactive(self):
        """Run pipeline in interactive mode"""
        
        while True:
            self.print_pipeline_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                self._run_conversion_interactive()
            elif choice == "2":
                self._run_filter_interactive()
            elif choice == "3":
                self._run_removal_interactive()
            elif choice == "4":
                self._run_duration_interactive()
            elif choice == "5":
                self._run_full_pipeline_interactive()
            elif choice == "6":
                print("Exiting pipeline...")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _run_conversion_interactive(self):
        """Interactive conversion"""
        from .utils.helpers import get_user_input
        
        input_dir = get_user_input("Input folder path: ", is_path=True)
        output_dir = get_user_input("Output folder path: ")
        input_fmt = input("Input format (default: mp3): ").strip() or "mp3"
        output_fmt = input("Output format (default: wav): ").strip() or "wav"
        
        result = self.run_conversion_step(input_dir, output_dir, input_fmt, output_fmt)
        print(f"\n✅ Conversion complete: {result['success']}/{result['total']} successful")
    
    def _run_filter_interactive(self):
        """Interactive filtering"""
        from .utils.helpers import get_user_input
        
        input_dir = get_user_input("Folder path: ", is_path=True)
        min_dur = input("Minimum duration in seconds (default: 2.0): ").strip()
        min_dur = float(min_dur) if min_dur else 2.0
        
        result = self.run_filter_step(input_dir, min_dur)
        print(f"\n✅ Filtering complete")
    
    def _run_removal_interactive(self):
        """Interactive background removal"""
        from .utils.helpers import get_user_input
        
        input_dir = get_user_input("Input folder path: ", is_path=True)
        output_dir = get_user_input("Output folder path: ")
        model = input("Model file (default: model_bs_roformer_ep_317_sdr_12.9755.ckpt): ").strip()
        model = model or "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
        
        result = self.run_background_removal_step(input_dir, output_dir, model)
        print(f"\n✅ Background removal complete: {result['success']} successful")
    
    def _run_duration_interactive(self):
        """Interactive duration calculation"""
        from .utils.helpers import get_user_input
        
        input_dir = get_user_input("Folder path: ", is_path=True)
        result = self.run_duration_calculation_step(input_dir)
        print(f"\n✅ Duration: {result['formatted_duration']}")
    
    def _run_full_pipeline_interactive(self):
        """Run full pipeline interactively"""
        from .utils.helpers import get_user_input
        
        print("\nRunning FULL PIPELINE (4 steps)...")
        
        # Step 1: Conversion
        input_dir = get_user_input("Input folder (MP3 files): ", is_path=True)
        converted_dir = get_user_input("Converted output folder: ")
        
        print("\n[1/4] Converting MP3 to WAV...")
        conv_result = self.run_conversion_step(input_dir, converted_dir, "mp3", "wav")
        
        # Step 2: Filtering
        print("\n[2/4] Filtering short files...")
        min_dur = input("Minimum duration (default: 2.0s): ").strip()
        min_dur = float(min_dur) if min_dur else 2.0
        self.run_filter_step(converted_dir, min_dur)
        
        # Step 3: Background removal
        print("\n[3/4] Removing background noise...")
        clean_dir = get_user_input("Output folder for clean audio: ")
        model = input("Model file (default: model_bs_roformer_ep_317_sdr_12.9755.ckpt): ").strip()
        model = model or "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
        removal_result = self.run_background_removal_step(converted_dir, clean_dir, model)
        
        # Step 4: Duration calculation
        print("\n[4/4] Calculating duration...")
        dur_result = self.run_duration_calculation_step(clean_dir)
        
        # Summary
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)
        print(f"Step 1 - Converted: {conv_result['success']} files")
        print(f"Step 2 - Filtered: Done")
        print(f"Step 3 - Background removed: {removal_result['success']} files")
        print(f"Step 4 - Total duration: {dur_result['formatted_duration']}")
        print("=" * 60)


def main():
    """Main entry point"""
    pipeline = AudioPipeline()
    pipeline.run_interactive()


if __name__ == "__main__":
    main()
