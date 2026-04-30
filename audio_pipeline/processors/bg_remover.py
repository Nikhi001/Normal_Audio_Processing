"""
Background noise removal processor
"""

import os
import sys
import shutil
import logging
from typing import Optional, Dict
from pathlib import Path
from tqdm import tqdm

from ..config.settings import BACKGROUND_REMOVAL_CONFIG, CHECKPOINT_CONFIG
from ..utils.helpers import FileScanner, CheckpointManager, LoggerSetup


class BackgroundRemover:
    """Removes background noise from audio files using audio-separator"""
    
    def __init__(self):
        self.config = BACKGROUND_REMOVAL_CONFIG
        self.checkpoint_manager = CheckpointManager(CHECKPOINT_CONFIG.checkpoint_file)
        self.logger = LoggerSetup.setup_logger("BackgroundRemover")
        
        try:
            import torch
            from audio_separator.separator import Separator
            self.Separator = Separator
            self.torch = torch
            self._check_gpu()
        except ImportError:
            self.logger.error("Required packages not installed. Install: audio-separator, torch")
            raise
    
    def _check_gpu(self) -> bool:
        """Check GPU availability"""
        if self.torch.cuda.is_available():
            gpu_name = self.torch.cuda.get_device_name(0)
            cuda_version = self.torch.version.cuda
            self.logger.info(f"GPU available: {gpu_name} | CUDA: {cuda_version}")
            return True
        else:
            self.logger.warning("GPU not available, using CPU")
            return False
    
    def _is_already_processed(self, filename: str, output_folder: str) -> bool:
        """Check if vocal file already exists"""
        base_name = os.path.splitext(filename)[0]
        expected_file = f"{base_name}{self.config.output_suffix}.wav"
        return os.path.exists(os.path.join(output_folder, expected_file))
    
    def process_file(self, separator, input_path: str, filename: str, 
                    output_folder: str, checkpoint: Dict, pbar=None) -> str:
        """Process a single audio file"""
        try:
            if self._is_already_processed(filename, output_folder):
                self.checkpoint_manager.mark_processed(checkpoint, input_path)
                if pbar:
                    pbar.set_postfix_str(f"Skipped: {filename}")
                    pbar.update(1)
                return 'skipped'
            
            if self.checkpoint_manager.is_processed(checkpoint, input_path):
                if pbar:
                    pbar.set_postfix_str(f"Skipped: {filename}")
                    pbar.update(1)
                return 'skipped'
            
            base_name = os.path.splitext(filename)[0]
            output_name = f"{base_name}{self.config.output_suffix}"
            
            if pbar:
                pbar.set_postfix_str(f"Processing: {filename}")
            
            # Separate audio
            output_files = separator.separate(input_path, {"Vocals": output_name})
            
            # Move vocals to output folder
            for file_path in output_files:
                if file_path and os.path.exists(file_path):
                    if 'Vocals' in file_path or output_name in file_path:
                        destination = os.path.join(output_folder, os.path.basename(file_path))
                        shutil.move(file_path, destination)
                    else:
                        if os.path.exists(file_path):
                            os.remove(file_path)
            
            self.checkpoint_manager.mark_processed(checkpoint, input_path)
            
            if pbar:
                pbar.set_postfix_str(f"Done: {filename}")
                pbar.update(1)
            
            return 'success'
            
        except Exception as e:
            self.logger.error(f"Error processing {filename}: {str(e)}")
            if pbar:
                pbar.set_postfix_str(f"Failed: {filename}")
                pbar.update(1)
            return 'failed'
    
    def process_directory(self, input_dir: str, output_dir: str, 
                         model_file: str, recursive: bool = True) -> Dict:
        """Process all audio files in directory"""
        
        self.logger.info(f"Starting background removal from {input_dir}")
        
        # Load checkpoint
        checkpoint = self.checkpoint_manager.load()
        already_done = len(checkpoint.get("processed_files", []))
        
        if already_done > 0:
            self.logger.info(f"Checkpoint loaded: {already_done} file(s) already processed")
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Find audio files
        wav_files = FileScanner.find_files(input_dir, (".wav",), recursive)
        
        if not wav_files:
            self.logger.warning("No WAV files found")
            return {"total": 0, "success": 0, "skipped": 0, "failed": 0}
        
        # Load model
        try:
            self.logger.info(f"Loading model: {model_file}")
            separator = self.Separator()
            separator.load_model(model_filename=model_file)
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            raise
        
        success = 0
        failed = 0
        skipped = 0
        
        with tqdm(total=len(wav_files), desc="Processing", unit="file", colour="green") as pbar:
            for wav_file in wav_files:
                result = self.process_file(separator, wav_file, os.path.basename(wav_file),
                                         output_dir, checkpoint, pbar)
                
                if result == 'success':
                    success += 1
                elif result == 'skipped':
                    skipped += 1
                else:
                    failed += 1
        
        summary = {
            "total": len(wav_files),
            "success": success,
            "skipped": skipped,
            "failed": failed
        }
        
        self.logger.info(f"Processing complete: {success} successful, {skipped} skipped, {failed} failed")
        return summary


def main():
    """Command-line interface"""
    remover = BackgroundRemover()
    
    print("=" * 60)
    print("AUDIO BACKGROUND REMOVER (Vocal Separator)")
    print("=" * 60 + "\n")
    
    from ..utils.helpers import get_user_input
    
    input_folder = get_user_input("Enter input folder path: ", is_path=True)
    output_folder = get_user_input("Enter output folder path: ")
    model_file = input("Enter model file (default: model_bs_roformer_ep_317_sdr_12.9755.ckpt): ").strip()
    model_file = model_file or "model_bs_roformer_ep_317_sdr_12.9755.ckpt"
    
    result = remover.process_directory(input_folder, output_folder, model_file)
    
    print("\n" + "=" * 60)
    print(f"Total files: {result['total']}")
    print(f"Successful: {result['success']}")
    print(f"Skipped: {result['skipped']}")
    print(f"Failed: {result['failed']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
