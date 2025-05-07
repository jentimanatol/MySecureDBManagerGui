#!/usr/bin/env python
"""
Main entry point for the User Management System GUI application.
"""

import tkinter as tk
from tkinter import messagebox

from gui.login_screen import LoginScreen
from utils.config import AppConfig

def main():
    """Initialize and run the application."""
    # Create the main application window
    root = tk.Tk()
    root.title("User Management System")
    root.geometry("800x600")
    root.minsize(800, 600)
    
    # Initialize app configuration
    config = AppConfig()

    # Set app icon if available
    try:
        root.iconbitmap("assets/icon.ico")
    except tk.TclError:
        pass  # Icon file not found, continue without setting icon
        
    # Apply theme settings
    style = config.apply_theme(root)

    # Start with the login screen
    app = LoginScreen(root, config)
    
    # Start the application main loop
    root.mainloop()

if __name__ == "__main__":
    main()