"""
Audio duration calculator processor
"""

import os
import logging
from typing import Dict, List, Tuple
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import soundfile as sf
from tqdm import tqdm

from ..config.settings import AUDIO_DURATION_CONFIG
from ..utils.helpers import FileScanner, LoggerSetup, format_duration


class DurationCalculator:
    """Calculate total duration of audio files"""
    
    def __init__(self):
        self.config = AUDIO_DURATION_CONFIG
        self.logger = LoggerSetup.setup_logger("DurationCalculator")
    
    def get_duration(self, filepath: str) -> float:
        """Get duration of a single audio file"""
        try:
            with sf.SoundFile(filepath) as f:
                return len(f) / f.samplerate
        except Exception as e:
            self.logger.warning(f"Could not read {filepath}: {str(e)}")
            return 0
    
    def calculate_directory_duration(self, folder: str, recursive: bool = True) -> Dict:
        """Calculate total duration for all audio files in directory"""
        
        self.logger.info(f"Calculating duration for: {folder}")
        
        # Find audio files
        files = FileScanner.find_files(folder, self.config.supported_extensions, recursive)
        
        if not files:
            self.logger.warning("No audio files found")
            return {"total_files": 0, "total_duration": 0, "formatted_duration": "0 hr 0 min 0 sec"}
        
        self.logger.info(f"Found {len(files)} audio files")
        
        # Parallel processing
        durations = []
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            futures = {executor.submit(self.get_duration, f): f for f in files}
            
            with tqdm(total=len(files), desc="Reading", unit="file", colour="yellow") as pbar:
                for future in as_completed(futures):
                    file_path = futures[future]
                    duration = future.result()
                    durations.append(duration)
                    
                    pbar.set_postfix_str(os.path.basename(file_path)[:30])
                    pbar.update(1)
        
        total_duration = sum(durations)
        
        return {
            "total_files": len(files),
            "total_duration": total_duration,
            "formatted_duration": format_duration(total_duration),
            "average_duration": total_duration / len(files) if files else 0
        }
    
    def calculate_multiple_directories(self, folders: List[str]) -> Dict:
        """Calculate duration for multiple directories"""
        
        results = {}
        grand_total_files = 0
        grand_total_duration = 0
        
        print("\n" + "=" * 60)
        print("AUDIO DURATION CALCULATOR")
        print("=" * 60 + "\n")
        
        for folder in folders:
            if not os.path.exists(folder):
                self.logger.warning(f"Folder not found: {folder}")
                continue
            
            print(f"📁 {folder}")
            result = self.calculate_directory_duration(folder, self.config.include_subfolders)
            results[folder] = result
            
            print(f"   🎵 Files: {result['total_files']}")
            print(f"   ⏱️  Duration: {result['formatted_duration']}\n")
            
            grand_total_files += result['total_files']
            grand_total_duration += result['total_duration']
        
        # Print grand total
        print("=" * 60)
        print(f"📊 TOTAL | Files: {grand_total_files} | Duration: {format_duration(grand_total_duration)}")
        print("=" * 60)
        
        return {
            "by_folder": results,
            "grand_total_files": grand_total_files,
            "grand_total_duration": grand_total_duration,
            "formatted_total": format_duration(grand_total_duration)
        }


def main():
    """Command-line interface"""
    calculator = DurationCalculator()
    
    print("=" * 60)
    print("AUDIO DURATION CALCULATOR")
    print("=" * 60 + "\n")
    
    from ..utils.helpers import get_user_input
    
    single_or_multiple = input("Calculate (1) single folder or (2) multiple folders? Enter 1 or 2: ").strip()
    
    if single_or_multiple == "1":
        folder = get_user_input("Enter folder path: ", is_path=True)
        result = calculator.calculate_directory_duration(folder)
        
        print("\n" + "=" * 60)
        print(f"Total files: {result['total_files']}")
        print(f"Total duration: {result['formatted_duration']}")
        print(f"Average file: {format_duration(result['average_duration'])}")
        print("=" * 60)
    else:
        folders = []
        while True:
            folder = input("Enter folder path (or 'done' to finish): ").strip()
            if folder.lower() == 'done':
                break
            if os.path.exists(folder):
                folders.append(folder)
            else:
                print("Folder not found")
        
        if folders:
            calculator.calculate_multiple_directories(folders)


if __name__ == "__main__":
    main()
