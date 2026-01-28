"""
Flask Server Wrapper Module

Provides server lifecycle management for GUI integration:
- Start/stop Flask server in background thread
- Log capture and forwarding to callback
- Clean shutdown handling

Author: Course Platform Team
Version: 1.0
"""

import os
import sys
import threading
import logging
import io
import time
from typing import Callable, Optional
from werkzeug.serving import make_server

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class FlaskServerWrapper:
    """Wrapper class to manage Flask server lifecycle."""
    
    def __init__(self, log_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize the server wrapper.
        
        Args:
            log_callback: Optional callback function for log messages
        """
        self.server = None
        self.server_thread = None
        self.log_callback = log_callback
        self.is_running = False
        self._app = None
        self._log_stream = None
        
    def _setup_logging(self):
        """Configure logging to capture Flask output."""
        # Create a custom log handler that forwards to callback
        if self.log_callback:
            class CallbackHandler(logging.Handler):
                def __init__(handler_self, callback):
                    super().__init__()
                    handler_self.callback = callback
                    
                def emit(handler_self, record):
                    try:
                        msg = handler_self.format(record)
                        handler_self.callback(msg)
                    except Exception:
                        pass
            
            # Setup handler for Flask/Werkzeug logs
            handler = CallbackHandler(self.log_callback)
            handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S'))
            
            # Add to relevant loggers
            for logger_name in ['werkzeug', 'flask.app', 'app']:
                logger = logging.getLogger(logger_name)
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
    
    def _log(self, message: str):
        """Send log message to callback."""
        if self.log_callback:
            self.log_callback(message)
        print(message)
    
    def start(self, host: str = '127.0.0.1', port: int = 5000) -> bool:
        """
        Start the Flask server in a background thread.
        
        Args:
            host: Host address to bind to (default: localhost only)
            port: Port number (default: 5000)
            
        Returns:
            bool: True if server started successfully
        """
        if self.is_running:
            self._log("[SERVER] Server is already running")
            return False
        
        try:
            # Import app here to avoid circular imports and ensure fresh config
            from app import app
            self._app = app
            
            # Setup logging
            self._setup_logging()
            
            # Disable Flask's default startup messages
            import logging as log
            log.getLogger('werkzeug').setLevel(log.WARNING)
            
            # Create server
            self.server = make_server(host, port, app, threaded=True)
            self.server.timeout = 1  # Allow periodic checks
            
            # Start server in background thread
            def run_server():
                self._log(f"[SERVER] Starting on http://{host}:{port}")
                self.is_running = True
                try:
                    self.server.serve_forever()
                except Exception as e:
                    self._log(f"[SERVER] Error: {e}")
                finally:
                    self.is_running = False
                    self._log("[SERVER] Stopped")
            
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            
            # Wait briefly for server to start
            time.sleep(0.5)
            
            if self.is_running:
                self._log(f"[SERVER] Running at http://{host}:{port}")
                return True
            else:
                self._log("[SERVER] Failed to start")
                return False
                
        except Exception as e:
            self._log(f"[SERVER] Failed to start: {e}")
            return False
    
    def stop(self) -> bool:
        """
        Stop the Flask server gracefully.
        
        Returns:
            bool: True if server stopped successfully
        """
        if not self.is_running or not self.server:
            self._log("[SERVER] Server is not running")
            return False
        
        try:
            self._log("[SERVER] Shutting down...")
            self.server.shutdown()
            
            # Wait for thread to finish
            if self.server_thread:
                self.server_thread.join(timeout=5)
            
            self.is_running = False
            self.server = None
            self.server_thread = None
            self._log("[SERVER] Shutdown complete")
            return True
            
        except Exception as e:
            self._log(f"[SERVER] Error during shutdown: {e}")
            return False
    
    def is_server_running(self) -> bool:
        """Check if server is currently running."""
        return self.is_running
    
    def get_url(self, host: str = '127.0.0.1', port: int = 5000) -> str:
        """Get the server URL."""
        return f"http://{host}:{port}"


# Global server instance for module-level access
_server_instance: Optional[FlaskServerWrapper] = None


def get_server(log_callback: Optional[Callable[[str], None]] = None) -> FlaskServerWrapper:
    """
    Get or create the global server instance.
    
    Args:
        log_callback: Optional callback for log messages
        
    Returns:
        FlaskServerWrapper: Server instance
    """
    global _server_instance
    if _server_instance is None:
        _server_instance = FlaskServerWrapper(log_callback)
    elif log_callback:
        _server_instance.log_callback = log_callback
    return _server_instance


def start_server(log_callback: Optional[Callable[[str], None]] = None,
                 host: str = '127.0.0.1', port: int = 5000) -> bool:
    """
    Convenience function to start the server.
    
    Args:
        log_callback: Optional callback for log messages
        host: Host address
        port: Port number
        
    Returns:
        bool: True if started successfully
    """
    server = get_server(log_callback)
    return server.start(host, port)


def stop_server() -> bool:
    """
    Convenience function to stop the server.
    
    Returns:
        bool: True if stopped successfully
    """
    global _server_instance
    if _server_instance:
        return _server_instance.stop()
    return False


def is_running() -> bool:
    """Check if server is running."""
    global _server_instance
    return _server_instance.is_running if _server_instance else False
