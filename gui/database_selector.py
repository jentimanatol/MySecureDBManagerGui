"""
Database selector screen for the User Management System.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import re

from gui.main_app import MainApp


class DatabaseSelector:
    """Screen for selecting or creating a database."""
    
    def __init__(self, root, parent_frame, db_manager, config):
        """Initialize database selector screen.
        
        Args:
            root: Tkinter root window
            parent_frame: Parent frame to place widgets in
            db_manager: Database manager instance
            config: Application configuration object
        """
        self.root = root
        self.parent_frame = parent_frame
        self.db_manager = db_manager
        self.config = config
        
        # Update window title
        self.root.title("User Management System - Select Database")
        
        # Create widgets
        self._create_widgets()
        
    def _create_widgets(self):
        """Create screen widgets."""
        # Title
        title_label = ttk.Label(self.parent_frame, text="Select Database", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Get available databases
        self.databases = self.db_manager.get_all_databases()
        
        # Database selection frame
        db_frame = ttk.Frame(self.parent_frame)
        db_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create scrollable frame for databases
        container = ttk.Frame(db_frame)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add database buttons
        if self.databases:
            for db_name in self.databases:
                db_button = ttk.Button(
                    scrollable_frame,
                    text=db_name,
                    command=lambda name=db_name: self._select_database(name),
                    width=30
                )
                db_button.pack(pady=5, padx=10, fill=tk.X)
        else:
            no_db_label = ttk.Label(
                scrollable_frame,
                text="No databases found. Create a new one.",
                style="Subtitle.TLabel"
            )
            no_db_label.pack(pady=20)
        
        # Buttons frame
        button_frame = ttk.Frame(self.parent_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # New database button
        new_db_button = ttk.Button(
            button_frame,
            text="Create New Database",
            command=self._create_new_database,
            style="Primary.TButton"
        )
        new_db_button.pack(side=tk.RIGHT, padx=5)
        
        # Back button
        back_button = ttk.Button(
            button_frame,
            text="Back to Login",
            command=self._back_to_login
        )
        back_button.pack(side=tk.LEFT, padx=5)
    
    def _select_database(self, db_name):
        """Select an existing database and proceed to main app.
        
        Args:
            db_name: Name of the database to select
        """
        if self.db_manager.select_database(db_name):
            # Ensure tables exist
            if self.db_manager.create_tables():
                # Save last used database
                self.config.set("last_database", db_name)
                
                # Open main application
                self._open_main_app()
            else:
                messagebox.showerror("Error", f"Failed to create tables in database {db_name}")
        else:
            messagebox.showerror("Error", f"Failed to select database {db_name}")
    
    def _create_new_database(self):
        """Create a new database."""
        # Ask for database name
        db_name = simpledialog.askstring(
            "New Database",
            "Enter a name for the new database:",
            parent=self.root
        )
        
        if not db_name:
            return
        
        # Validate database name
        if not re.match(r'^\w+$', db_name):
            messagebox.showerror(
                "Invalid Name",
                "Database name can only contain letters, numbers, and underscores"
            )
            return
        
        # Try to create database
        if self.db_manager.create_database(db_name):
            # Create tables
            if self.db_manager.create_tables():
                # Save last used database
                self.config.set("last_database", db_name)
                
                messagebox.showinfo("Success", f"Database '{db_name}' created successfully!")
                
                # Open main application
                self._open_main_app()
            else:
                messagebox.showerror("Error", "Failed to create tables in new database")
        else:
            messagebox.showerror("Error", "Failed to create new database")
    
    def _open_main_app(self):
        """Open the main application."""
        # Clear current screen
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create main application screen
        MainApp(self.root, self.parent_frame, self.db_manager, self.config)
    
    def _back_to_login(self):
        """Go back to login screen."""
        # Close database connection
        self.db_manager.close_connection()
        
        # Recreate login screen
        from gui.login_screen import LoginScreen
        
        # Clear current screen
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        
        # Create login screen
        LoginScreen(self.root, self.config)