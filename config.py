"""
Configuration Management Module

Handles persistent storage of application settings including:
- Static folder path selection
- Cross-platform config directory detection
- Safe path validation and handling

Author: Course Platform Team
Version: 1.0
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any


# Application identifier for config directory
APP_NAME = "OfflineCoursePlayer"


def get_config_dir() -> Path:
    """
    Get the platform-appropriate configuration directory.
    
    Returns:
        Path: Configuration directory path
        - Windows: %APPDATA%/OfflineCoursePlayer
        - macOS: ~/Library/Application Support/OfflineCoursePlayer
        - Linux: ~/.config/OfflineCoursePlayer
    """
    if sys.platform == "win32":
        # Windows: Use APPDATA
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        config_dir = Path(base) / APP_NAME
    elif sys.platform == "darwin":
        # macOS: Use Application Support
        config_dir = Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        # Linux and others: Use .config
        xdg_config = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        config_dir = Path(xdg_config) / APP_NAME
    
    # Ensure directory exists
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the path to the configuration file."""
    return get_config_dir() / "config.json"


def get_database_path() -> Path:
    """
    Get the path for the SQLite database.
    
    Returns:
        Path: Database file path in config directory
    """
    return get_config_dir() / "course_progress.db"


def load_config() -> Dict[str, Any]:
    """
    Load configuration from file.
    
    Returns:
        Dict: Configuration dictionary, empty if file doesn't exist
    """
    config_file = get_config_file()
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[CONFIG] Error loading config: {e}")
            return {}
    return {}


def save_config(config: Dict[str, Any]) -> bool:
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary to save
        
    Returns:
        bool: True if save successful, False otherwise
    """
    config_file = get_config_file()
    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        return True
    except IOError as e:
        print(f"[CONFIG] Error saving config: {e}")
        return False


def get_static_folder() -> Optional[str]:
    """
    Get the configured static folder path.
    
    Returns:
        Optional[str]: Configured static folder path, or None if not set
    """
    config = load_config()
    folder = config.get("static_folder")
    
    # Validate folder still exists
    if folder and os.path.isdir(folder):
        return folder
    return None


def set_static_folder(path: str) -> bool:
    """
    Set and persist the static folder path.
    
    Args:
        path: Absolute path to the static folder
        
    Returns:
        bool: True if save successful, False otherwise
    """
    # Validate path
    if not validate_folder(path):
        return False
    
    config = load_config()
    config["static_folder"] = os.path.abspath(path)
    return save_config(config)


def validate_folder(path: str) -> bool:
    """
    Validate that a folder path is valid and accessible.
    
    Args:
        path: Path to validate
        
    Returns:
        bool: True if valid and accessible, False otherwise
    """
    if not path:
        return False
    
    try:
        # Normalize and resolve path
        resolved = os.path.abspath(path)
        
        # Check if directory exists and is readable
        if not os.path.isdir(resolved):
            return False
        
        # Check read access
        if not os.access(resolved, os.R_OK):
            return False
        
        return True
    except (OSError, ValueError) as e:
        print(f"[CONFIG] Path validation error: {e}")
        return False


def get_app_directory() -> Path:
    """
    Get the application's installation directory.
    
    Returns:
        Path: Directory containing the application files
    """
    # Get directory of the main script
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent.resolve()


def get_default_static_folder() -> Optional[str]:
    """
    Get the default static folder (./static relative to app).
    
    Returns:
        Optional[str]: Default static folder if it exists, None otherwise
    """
    app_dir = get_app_directory()
    default_static = app_dir / "static"
    
    if default_static.exists() and default_static.is_dir():
        return str(default_static)
    return None


# Convenience function to get the effective static folder
def get_effective_static_folder() -> str:
    """
    Get the effective static folder to use.
    
    Priority:
    1. User-configured folder
    2. Default ./static folder
    3. Empty string (caller should handle)
    
    Returns:
        str: Path to static folder, or empty string if none available
    """
    # Try user-configured folder first
    configured = get_static_folder()
    if configured:
        return configured
    
    # Fall back to default static folder
    default = get_default_static_folder()
    if default:
        return default
    
    return ""
