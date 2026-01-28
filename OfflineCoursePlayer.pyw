"""
Offline Course Player - One-Click Launcher

This is the primary entry point for the application.
Double-click this file to launch the desktop app.

Features:
- Auto-installs required dependencies on first run
- No console window (Windows .pyw)
- Cross-platform support

Author: Course Platform Team
Version: 1.0
"""

import sys
import os
import subprocess

# Ensure we're in the correct directory
APP_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(APP_DIR)


def check_dependency(module_name: str) -> bool:
    """Check if a Python module is installed."""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def install_dependencies():
    """Install required dependencies using pip."""
    dependencies = [
        ("flask", "flask"),
        ("PyQt6", "PyQt6"),
    ]
    
    missing = []
    for import_name, pip_name in dependencies:
        if not check_dependency(import_name):
            missing.append(pip_name)
    
    if not missing:
        return True
    
    # Show installation dialog using tkinter (always available)
    try:
        import tkinter as tk
        from tkinter import ttk
        
        root = tk.Tk()
        root.title("Offline Course Player - Setup")
        root.geometry("400x150")
        root.resizable(False, False)
        
        # Center window
        root.eval('tk::PlaceWindow . center')
        
        # Configure dark theme
        root.configure(bg='#2d2d2d')
        
        style = ttk.Style()
        style.configure('TLabel', background='#2d2d2d', foreground='white')
        style.configure('TProgressbar', troughcolor='#444', background='#4CAF50')
        
        # Title
        title_label = tk.Label(
            root, 
            text="📚 Installing Dependencies...", 
            font=('Segoe UI', 14, 'bold'),
            bg='#2d2d2d',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Status
        status_label = tk.Label(
            root,
            text=f"Installing: {', '.join(missing)}",
            font=('Segoe UI', 10),
            bg='#2d2d2d',
            fg='#aaa'
        )
        status_label.pack(pady=5)
        
        # Progress bar
        progress = ttk.Progressbar(root, mode='indeterminate', length=300)
        progress.pack(pady=20)
        progress.start(10)
        
        root.update()
        
        # Install packages
        success = True
        for package in missing:
            status_label.config(text=f"Installing: {package}")
            root.update()
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                if result.returncode != 0:
                    success = False
                    break
            except Exception as e:
                success = False
                break
        
        progress.stop()
        root.destroy()
        
        if not success:
            # Show error dialog
            error_root = tk.Tk()
            error_root.withdraw()
            from tkinter import messagebox
            messagebox.showerror(
                "Installation Failed",
                f"Failed to install dependencies.\n\nPlease run manually:\npip install {' '.join(missing)}"
            )
            error_root.destroy()
            return False
        
        return True
        
    except Exception as e:
        # Fallback: Just try pip install without GUI
        print(f"Installing dependencies: {missing}")
        for package in missing:
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", package],
                    check=True
                )
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}")
                return False
        return True


def main():
    """Main entry point."""
    # First, check and install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Now import and run the desktop app
    try:
        from desktop_app import main as run_app
        run_app()
    except ImportError as e:
        # Show error if import fails
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Launch Error",
                f"Failed to start application:\n{e}\n\nPlease ensure all files are present."
            )
            root.destroy()
        except:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
