"""
Audio file filter processor - Remove short/invalid audio files
"""

import os
import logging
from typing import Dict, List
from pathlib import Path
import soundfile as sf
from tqdm import tqdm

from ..config.settings import AUDIO_FILTER_CONFIG
from ..utils.helpers import FileScanner, LoggerSetup, format_duration


class AudioFilter:
    """Filters audio files based on criteria (duration, validity, etc.)"""
    
    def __init__(self, min_duration: float = None):
        self.config = AUDIO_FILTER_CONFIG
        self.min_duration = min_duration or self.config.min_duration_seconds
        self.logger = LoggerSetup.setup_logger("AudioFilter")
    
    def get_file_duration(self, filepath: str) -> float:
        """Get duration of audio file"""
        try:
            info = sf.info(filepath)
            return info.duration
        except Exception as e:
            self.logger.warning(f"Could not read {filepath}: {str(e)}")
            return -1  # Mark as invalid
    
    def is_valid_audio(self, filepath: str) -> bool:
        """Check if file is valid audio"""
        try:
            sf.info(filepath)
            return True
        except:
            return False
    
    def filter_directory(self, folder: str, min_duration: float = None, 
                        recursive: bool = False, dry_run: bool = True) -> Dict:
        """Filter and remove short/invalid files from directory"""
        
        min_duration = min_duration or self.min_duration
        self.logger.info(f"Filtering files in {folder} (min duration: {min_duration}s)")
        
        # Find audio files
        files = FileScanner.find_files(folder, self.config.supported_extensions, recursive)
        
        if not files:
            self.logger.warning("No audio files found")
            return {"total": 0, "short_files": [], "invalid_files": []}
        
        short_files = []
        invalid_files = []
        
        with tqdm(total=len(files), desc="Scanning", unit="file", colour="cyan") as pbar:
            for filepath in files:
                pbar.set_postfix(file=os.path.basename(filepath)[:40])
                
                if not self.is_valid_audio(filepath):
                    invalid_files.append(filepath)
                else:
                    duration = self.get_file_duration(filepath)
                    if duration < min_duration:
                        short_files.append((filepath, duration))
                
                pbar.update(1)
        
        # Print summary
        print("\n" + "=" * 60)
        print("FILTER RESULTS")
        print("=" * 60)
        print(f"Total files scanned: {len(files)}")
        print(f"Short files (< {min_duration}s): {len(short_files)}")
        print(f"Invalid files: {len(invalid_files)}")
        print("=" * 60)
        
        if invalid_files:
            print("\nInvalid files:")
            for f in invalid_files[:5]:
                print(f"  - {os.path.relpath(f, folder)}")
            if len(invalid_files) > 5:
                print(f"  ... and {len(invalid_files) - 5} more")
        
        if short_files:
            print(f"\nShort files (< {min_duration}s):")
            for filepath, duration in short_files[:5]:
                print(f"  - {os.path.relpath(filepath, folder)} ({format_duration(duration)})")
            if len(short_files) > 5:
                print(f"  ... and {len(short_files) - 5} more")
        
        if not dry_run:
            all_to_delete = short_files + [(f, 0) for f in invalid_files]
            
            if all_to_delete:
                confirm = input(f"\nDelete all {len(all_to_delete)} files? (yes/no): ").strip().lower()
                if confirm in ("yes", "y"):
                    for filepath, _ in all_to_delete:
                        try:
                            os.remove(filepath)
                            self.logger.info(f"Deleted: {filepath}")
                        except Exception as e:
                            self.logger.error(f"Could not delete {filepath}: {str(e)}")
                    
                    print(f"\n✅ Deleted {len(all_to_delete)} file(s)")
                else:
                    print("Deletion cancelled")
        
        return {
            "total": len(files),
            "short_files": short_files,
            "invalid_files": invalid_files,
            "min_duration": min_duration
        }


def main():
    """Command-line interface"""
    
    print("=" * 60)
    print("AUDIO FILE FILTER (Remove short/invalid files)")
    print("=" * 60 + "\n")
    
    from ..utils.helpers import get_user_input
    
    folder = get_user_input("Enter folder path: ", is_path=True)
    min_duration = input("Enter minimum duration in seconds (default: 2.0): ").strip()
    min_duration = float(min_duration) if min_duration else 2.0
    
    recursive = input("Include subfolders? (yes/no, default: no): ").strip().lower() in ("yes", "y")
    
    dry_run = input("Perform dry run? (yes/no, default: yes): ").strip().lower() != "no"
    
    filter_processor = AudioFilter(min_duration)
    filter_processor.filter_directory(folder, min_duration, recursive, dry_run)


if __name__ == "__main__":
    main()
