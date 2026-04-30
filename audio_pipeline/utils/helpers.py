"""
Utility functions for audio pipeline
"""

import os
import json
import logging
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class CheckpointManager:
    """Manages checkpoint files for resumable processing"""
    
    def __init__(self, checkpoint_file: str):
        self.checkpoint_file = checkpoint_file
        self.checkpoint_dir = Path(checkpoint_file).parent
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> Dict[str, Any]:
        """Load checkpoint from JSON file"""
        if Path(self.checkpoint_file).exists():
            with open(self.checkpoint_file, 'r') as f:
                return json.load(f)
        return {"processed_files": [], "failed_files": [], "timestamp": str(datetime.now())}
    
    def save(self, checkpoint: Dict[str, Any]) -> None:
        """Save checkpoint to JSON file"""
        checkpoint["timestamp"] = str(datetime.now())
        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=4)
    
    def mark_processed(self, checkpoint: Dict[str, Any], filepath: str) -> None:
        """Mark a file as processed"""
        if filepath not in checkpoint["processed_files"]:
            checkpoint["processed_files"].append(filepath)
            self.save(checkpoint)
    
    def mark_failed(self, checkpoint: Dict[str, Any], filepath: str, error: str) -> None:
        """Mark a file as failed"""
        if "failed_files" not in checkpoint:
            checkpoint["failed_files"] = {}
        checkpoint["failed_files"][filepath] = error
        self.save(checkpoint)
    
    def is_processed(self, checkpoint: Dict[str, Any], filepath: str) -> bool:
        """Check if file is already processed"""
        return filepath in checkpoint.get("processed_files", [])


class FileScanner:
    """Scans directories for audio files"""
    
    @staticmethod
    def extract_number(name: str) -> int:
        """Extract first number from string (for sorting)"""
        match = re.search(r'\d+', name)
        return int(match.group()) if match else float('inf')
    
    @staticmethod
    def get_sorted_subdirs(folder: str) -> List[str]:
        """Get and sort subdirectories numerically"""
        subdirs = [d for d in os.listdir(folder)
                   if os.path.isdir(os.path.join(folder, d))]
        subdirs.sort(key=FileScanner.extract_number)
        return subdirs
    
    @staticmethod
    def find_files(folder: str, extensions: tuple, recursive: bool = False) -> List[str]:
        """Find all files with given extensions"""
        files = []
        if recursive:
            for root, _, filenames in os.walk(folder):
                files.extend([os.path.join(root, f) for f in filenames
                            if f.lower().endswith(extensions)])
        else:
            files = [os.path.join(folder, f) for f in os.listdir(folder)
                    if f.lower().endswith(extensions)]
        return files
    
    @staticmethod
    def get_relative_path(file_path: str, base_path: str) -> str:
        """Get relative path for display"""
        try:
            return os.path.relpath(file_path, base_path)
        except ValueError:
            return file_path


class LoggerSetup:
    """Setup logging for the pipeline"""
    
    @staticmethod
    def setup_logger(name: str, log_file: Optional[str] = None, 
                     level: str = "INFO") -> logging.Logger:
        """Setup and return a logger instance"""
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level))
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level))
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add console handler
        if not logger.handlers:
            logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, level))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger


def format_duration(seconds: float) -> str:
    """Format seconds to human-readable duration"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours} hr {minutes} min {secs} sec"


def get_user_input(prompt: str, is_path: bool = False, required: bool = True) -> str:
    """Get input from user with optional validation"""
    while True:
        user_input = input(prompt).strip()
        
        if not user_input:
            if required:
                print("Input cannot be empty. Please try again.")
                continue
            return ""
        
        if is_path and not os.path.exists(user_input):
            print(f"Path does not exist: {user_input}")
            continue
        
        return user_input


def get_optional_input(prompt: str, default_value: str) -> str:
    """Get optional input with default value"""
    while True:
        print(f"\nDefault: {default_value}")
        choice = input(f"{prompt} (Press Enter to use default, or type 'custom'): ").strip().lower()
        
        if not choice or choice == '':
            return default_value
        elif choice == 'custom':
            custom = input("Enter custom value: ").strip()
            if custom:
                return custom
            print("Input cannot be empty. Please try again.")
        else:
            print("Invalid choice. Press Enter for default or type 'custom'.")
