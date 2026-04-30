"""
Audio conversion processor - Convert between audio formats
"""

import os
import logging
from typing import Optional
from pathlib import Path
from pydub import AudioSegment
from tqdm import tqdm

from ..config.settings import AUDIO_CONVERSION_CONFIG
from ..utils.helpers import FileScanner, LoggerSetup


class AudioConverter:
    """Converts audio files between different formats"""
    
    def __init__(self):
        self.config = AUDIO_CONVERSION_CONFIG
        self.logger = LoggerSetup.setup_logger("AudioConverter")
    
    def convert_file(self, input_path: str, output_path: str, 
                    output_format: str = "wav") -> bool:
        """Convert a single audio file"""
        try:
            self.logger.info(f"Converting: {os.path.basename(input_path)}")
            
            # Load audio file
            audio = AudioSegment.from_file(input_path)
            
            # Create output directory if needed
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Export to target format
            audio.export(output_path, format=output_format)
            self.logger.debug(f"Successfully converted to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error converting {input_path}: {str(e)}")
            return False
    
    def convert_directory(self, input_dir: str, output_dir: str, 
                         input_format: str = "mp3", output_format: str = "wav",
                         recursive: bool = False) -> dict:
        """Convert all audio files in a directory"""
        
        self.logger.info(f"Starting batch conversion from {input_dir}")
        
        # Find all files with input format
        files = FileScanner.find_files(input_dir, (f".{input_format}",), recursive)
        
        if not files:
            self.logger.warning(f"No {input_format} files found in {input_dir}")
            return {"total": 0, "success": 0, "failed": 0}
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        failed_count = 0
        
        with tqdm(files, desc="Converting", unit="file", colour="cyan") as pbar:
            for input_file in pbar:
                # Maintain directory structure if recursive
                if recursive:
                    rel_path = os.path.relpath(input_file, input_dir)
                    output_file = os.path.join(output_dir, 
                                             os.path.splitext(rel_path)[0] + f".{output_format}")
                else:
                    filename = os.path.basename(input_file)
                    output_file = os.path.join(output_dir, 
                                             os.path.splitext(filename)[0] + f".{output_format}")
                
                pbar.set_postfix(file=os.path.basename(input_file)[:30])
                
                if self.convert_file(input_file, output_file, output_format):
                    success_count += 1
                else:
                    failed_count += 1
        
        summary = {
            "total": len(files),
            "success": success_count,
            "failed": failed_count
        }
        
        self.logger.info(f"Conversion complete: {success_count}/{len(files)} successful")
        return summary


def main():
    """Command-line interface for audio conversion"""
    converter = AudioConverter()
    
    print("=" * 60)
    print("AUDIO CONVERTER (MP3 to WAV)")
    print("=" * 60 + "\n")
    
    from ..utils.helpers import get_user_input
    
    input_folder = get_user_input("Enter input folder path: ", is_path=True)
    output_folder = get_user_input("Enter output folder path: ")
    
    input_format = input("Enter input format (default: mp3): ").strip() or "mp3"
    output_format = input("Enter output format (default: wav): ").strip() or "wav"
    
    recursive = input("Include subfolders? (yes/no, default: no): ").strip().lower() in ("yes", "y")
    
    result = converter.convert_directory(input_folder, output_folder, 
                                        input_format, output_format, recursive)
    
    print("\n" + "=" * 60)
    print(f"Total files: {result['total']}")
    print(f"Successful: {result['success']}")
    print(f"Failed: {result['failed']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
