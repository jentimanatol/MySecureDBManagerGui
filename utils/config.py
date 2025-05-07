"""
Configuration settings for the application.
"""

import tkinter as tk
from tkinter import ttk
import os
import json


class AppConfig:
    """Class to handle application configuration settings."""
    
    def __init__(self):
        """Initialize configuration with default settings."""
        # Define default configuration
        self.config = {
            "theme": "light",
            "host": "localhost",
            "user": "root",
            "last_database": "",
            "window_size": "800x600"
        }
        
        # Create config directory if it doesn't exist
        os.makedirs(os.path.expanduser("~/.user_management_system"), exist_ok=True)
        self.config_file = os.path.expanduser("~/.user_management_system/config.json")
        
        # Load existing configuration if available
        self.load_config()
    
    def load_config(self):
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    # Update default config with loaded values
                    self.config.update(loaded_config)
        except Exception:
            # If loading fails, use default configuration
            pass
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
        except Exception:
            # If saving fails, continue silently
            pass
    
    def get(self, key, default=None):
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            The configuration value or default
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value and save configuration.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
        self.save_config()
    
    def apply_theme(self, root):
        """Apply the configured theme to the application.
        
        Args:
            root: Tkinter root window
            
        Returns:
            ttk.Style: The configured style object
        """
        style = ttk.Style(root)
        
        if self.get("theme") == "dark":
            # Dark theme configuration
            style.theme_use("clam")
            
            # Configure colors
            root.configure(bg="#2d2d2d")
            style.configure(".", 
                background="#2d2d2d", 
                foreground="#ffffff",
                fieldbackground="#3d3d3d")
            
            # Configure specific elements
            style.configure("TFrame", background="#2d2d2d")
            style.configure("TLabel", background="#2d2d2d", foreground="#ffffff")
            style.configure("TButton", background="#404040", foreground="#ffffff")
            style.map("TButton",
                background=[("active", "#505050"), ("disabled", "#2d2d2d")],
                foreground=[("disabled", "#808080")])
            
            style.configure("TEntry", fieldbackground="#3d3d3d", foreground="#ffffff")
            style.configure("TCombobox", fieldbackground="#3d3d3d", background="#404040", foreground="#ffffff")
            style.map("TCombobox", 
                fieldbackground=[("readonly", "#3d3d3d")],
                background=[("readonly", "#404040")])
            
            style.configure("Treeview", 
                background="#3d3d3d", 
                fieldbackground="#3d3d3d", 
                foreground="#ffffff")
            style.map("Treeview", 
                background=[("selected", "#505050")],
                foreground=[("selected", "#ffffff")])
                
            # Custom styles
            style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), background="#2d2d2d", foreground="#ffffff")
            style.configure("Subtitle.TLabel", font=("Helvetica", 12), background="#2d2d2d", foreground="#ffffff")
            style.configure("Header.TLabel", font=("Helvetica", 10, "bold"), background="#2d2d2d", foreground="#ffffff")
            
            style.configure("Primary.TButton", font=("Helvetica", 10, "bold"), background="#3b82f6", foreground="#ffffff")
            style.map("Primary.TButton",
                background=[("active", "#2563eb"), ("disabled", "#2d2d2d")],
                foreground=[("disabled", "#808080")])
                
            style.configure("Success.TButton", font=("Helvetica", 10), background="#10b981", foreground="#ffffff")
            style.map("Success.TButton",
                background=[("active", "#059669"), ("disabled", "#2d2d2d")],
                foreground=[("disabled", "#808080")])
                
            style.configure("Danger.TButton", font=("Helvetica", 10), background="#ef4444", foreground="#ffffff")
            style.map("Danger.TButton",
                background=[("active", "#dc2626"), ("disabled", "#2d2d2d")],
                foreground=[("disabled", "#808080")])
        else:
            # Light theme configuration (default)
            style.theme_use("clam")
            
            # Configure colors
            root.configure(bg="#f5f5f5")
            style.configure(".", 
                background="#f5f5f5", 
                foreground="#333333",
                fieldbackground="#ffffff")
            
            # Configure specific elements
            style.configure("TFrame", background="#f5f5f5")
            style.configure("TLabel", background="#f5f5f5", foreground="#333333")
            style.configure("TButton", background="#e0e0e0", foreground="#333333")
            style.map("TButton",
                background=[("active", "#d0d0d0"), ("disabled", "#f5f5f5")],
                foreground=[("disabled", "#a0a0a0")])
            
            style.configure("TEntry", fieldbackground="#ffffff", foreground="#333333")
            style.configure("TCombobox", fieldbackground="#ffffff", background="#e0e0e0", foreground="#333333")
            style.map("TCombobox", 
                fieldbackground=[("readonly", "#ffffff")],
                background=[("readonly", "#e0e0e0")])
            
            style.configure("Treeview", 
                background="#ffffff", 
                fieldbackground="#ffffff", 
                foreground="#333333")
            style.map("Treeview", 
                background=[("selected", "#0078d7")],
                foreground=[("selected", "#ffffff")])
                
            # Custom styles
            style.configure("Title.TLabel", font=("Helvetica", 16, "bold"), background="#f5f5f5", foreground="#333333")
            style.configure("Subtitle.TLabel", font=("Helvetica", 12), background="#f5f5f5", foreground="#333333")
            style.configure("Header.TLabel", font=("Helvetica", 10, "bold"), background="#f5f5f5", foreground="#333333")
            
            style.configure("Primary.TButton", font=("Helvetica", 10, "bold"), background="#3b82f6", foreground="#ffffff")
            style.map("Primary.TButton",
                background=[("active", "#2563eb"), ("disabled", "#f5f5f5")],
                foreground=[("disabled", "#a0a0a0")])
                
            style.configure("Success.TButton", font=("Helvetica", 10), background="#10b981", foreground="#ffffff")
            style.map("Success.TButton",
                background=[("active", "#059669"), ("disabled", "#f5f5f5")],
                foreground=[("disabled", "#a0a0a0")])
                
            style.configure("Danger.TButton", font=("Helvetica", 10), background="#ef4444", foreground="#ffffff")
            style.map("Danger.TButton",
                background=[("active", "#dc2626"), ("disabled", "#f5f5f5")],
                foreground=[("disabled", "#a0a0a0")])
        
        return style
        
    def toggle_theme(self, root):
        """Toggle between light and dark themes.
        
        Args:
            root: Tkinter root window
            
        Returns:
            str: The new theme name
        """
        current_theme = self.get("theme", "light")
        new_theme = "dark" if current_theme == "light" else "light"
        self.set("theme", new_theme)
        self.apply_theme(root)
        return new_theme