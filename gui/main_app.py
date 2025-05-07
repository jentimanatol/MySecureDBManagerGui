"""
Main application module for the User Management System.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from gui.users.user_list import UserListView
from gui.users.user_form import UserForm


class MainApp:
    """Main application class for the User Management System."""
    
    def __init__(self, root, parent_frame, db_manager, config):
        """Initialize main application.
        
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
        
        # Update window title with database name
        self.root.title(f"User Management System - {self.db_manager.db_name}")
        
        # Create UI structure
        self._create_structure()
        
        # Start with user list view
        self._show_user_list()
    
    def _create_structure(self):
        """Create the main application UI structure."""
        # Create main container with margins
        self.main_container = ttk.Frame(self.parent_frame, padding=10)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create header frame
        self.header_frame = ttk.Frame(self.main_container)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Database name and info
        db_label = ttk.Label(
            self.header_frame, 
            text=f"Database: {self.db_manager.db_name}", 
            style="Header.TLabel"
        )
        db_label.pack(side=tk.LEFT)
        
        # Create status bar at the bottom
        self.status_bar = ttk.Label(
            self.main_container, 
            text=f"Connected to {self.db_manager.db_name} | {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Create navigation frame (left sidebar)
        self.nav_frame = ttk.Frame(self.main_container, width=150)
        self.nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.nav_frame.pack_propagate(False)  # Prevent shrinking
        
        # Create navigation buttons
        self.nav_buttons = []
        
        # Users button
        users_btn = ttk.Button(
            self.nav_frame, 
            text="Users", 
            command=self._show_user_list
        )
        users_btn.pack(fill=tk.X, pady=2)
        self.nav_buttons.append(users_btn)
        
        # Add user button
        add_user_btn = ttk.Button(
            self.nav_frame, 
            text="Add User", 
            command=lambda: self._show_user_form()
        )
        add_user_btn.pack(fill=tk.X, pady=2)
        self.nav_buttons.append(add_user_btn)
        
        # Separator
        ttk.Separator(self.nav_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Settings button
        settings_btn = ttk.Button(
            self.nav_frame, 
            text="Settings", 
            command=self._show_settings
        )
        settings_btn.pack(fill=tk.X, pady=2)
        self.nav_buttons.append(settings_btn)
        
        # Logout button at the bottom
        ttk.Separator(self.nav_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        logout_btn = ttk.Button(
            self.nav_frame, 
            text="Logout", 
            command=self._logout
        )
        logout_btn.pack(fill=tk.X, pady=2)
        
        # Create main content frame
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def _update_status(self, message):
        """Update status bar message.
        
        Args:
            message: Message to display
        """
        self.status_bar.config(
            text=f"{message} | {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
    
    def _clear_content(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _show_user_list(self):
        """Show the user list view."""
        self._clear_content()
        self._update_status(f"Connected to {self.db_manager.db_name}")
        UserListView(self.content_frame, self.db_manager, self)
    
    def _show_user_form(self, user_id=None):
        """Show the user form (create or edit).
        
        Args:
            user_id: User ID to edit, or None for a new user
        """
        self._clear_content()
        if user_id:
            self._update_status(f"Editing user ID: {user_id}")
        else:
            self._update_status("Creating new user")
        UserForm(self.content_frame, self.db_manager, self, user_id)
    
    def _show_settings(self):
        """Show settings view."""
        self._clear_content()
        self._update_status("Settings")
        
        # Create settings frame
        settings_frame = ttk.Frame(self.content_frame, padding=20)
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            settings_frame, 
            text="Application Settings", 
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 20))
        
        # Theme settings
        theme_frame = ttk.LabelFrame(settings_frame, text="Theme Settings", padding=10)
        theme_frame.pack(fill=tk.X, pady=10)
        
        theme_button = ttk.Button(
            theme_frame,
            text=f"Toggle Theme (Current: {self.config.get('theme', 'light').title()})",
            command=lambda: self._toggle_theme(theme_button)
        )
        theme_button.pack(pady=5)
        
        # Connection settings
        conn_frame = ttk.LabelFrame(settings_frame, text="Connection Information", padding=10)
        conn_frame.pack(fill=tk.X, pady=10)
        
        host_label = ttk.Label(
            conn_frame,
            text=f"Host: {self.config.get('host', 'localhost')}"
        )
        host_label.pack(anchor=tk.W, pady=2)
        
        user_label = ttk.Label(
            conn_frame,
            text=f"User: {self.config.get('user', 'root')}"
        )
        user_label.pack(anchor=tk.W, pady=2)
        
        db_label = ttk.Label(
            conn_frame,
            text=f"Database: {self.db_manager.db_name}"
        )
        db_label.pack(anchor=tk.W, pady=2)
        
        # About section
        about_frame = ttk.LabelFrame(settings_frame, text="About", padding=10)
        about_frame.pack(fill=tk.X, pady=10)
        
        about_text = ttk.Label(
            about_frame,
            text="User Management System\nVersion 1.0\n\nCreated for educational purposes.",
            justify=tk.LEFT
        )
        about_text.pack(anchor=tk.W, pady=5)
    
    def _toggle_theme(self, button):
        """Toggle application theme.
        
        Args:
            button: Button to update text
        """
        new_theme = self.config.toggle_theme(self.root)
        button.config(text=f"Toggle Theme (Current: {new_theme.title()})")
    
    def _logout(self):
        """Logout and return to the database selection screen."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Go back to database selector
            from gui.database_selector import DatabaseSelector
            
            # Clear current screen
            for widget in self.parent_frame.winfo_children():
                widget.destroy()
            
            # Create database selector screen
            DatabaseSelector(self.root, self.parent_frame, self.db_manager, self.config)