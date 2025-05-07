"""
Login screen module for the User Management System.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re

from database.db_manager import DatabaseManager
from gui.database_selector import DatabaseSelector


class LoginScreen:
    """Login screen for connecting to MySQL server."""
    
    def __init__(self, root, config):
        """Initialize login screen.
        
        Args:
            root: Tkinter root window
            config: Application configuration object
        """
        self.root = root
        self.config = config
        self.db_manager = DatabaseManager()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create login form
        self._create_widgets()
        
    def _create_widgets(self):
        """Create screen widgets."""
        # Title
        title_label = ttk.Label(self.main_frame, text="MySQL Database Login", style="Title.TLabel")
        title_label.pack(pady=(0, 20))
        
        # Host frame
        host_frame = ttk.Frame(self.main_frame)
        host_frame.pack(fill=tk.X, pady=5)
        
        host_label = ttk.Label(host_frame, text="Host:", width=10)
        host_label.pack(side=tk.LEFT)
        
        self.host_var = tk.StringVar(value=self.config.get("host", "localhost"))
        host_entry = ttk.Entry(host_frame, textvariable=self.host_var)
        host_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Username frame
        user_frame = ttk.Frame(self.main_frame)
        user_frame.pack(fill=tk.X, pady=5)
        
        user_label = ttk.Label(user_frame, text="Username:", width=10)
        user_label.pack(side=tk.LEFT)
        
        self.user_var = tk.StringVar(value=self.config.get("user", "root"))
        user_entry = ttk.Entry(user_frame, textvariable=self.user_var)
        user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Password frame
        pass_frame = ttk.Frame(self.main_frame)
        pass_frame.pack(fill=tk.X, pady=5)
        
        pass_label = ttk.Label(pass_frame, text="Password:", width=10)
        pass_label.pack(side=tk.LEFT)
        
        self.pass_var = tk.StringVar()
        pass_entry = ttk.Entry(pass_frame, textvariable=self.pass_var, show="*")
        pass_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Show/Hide password
        self.show_password = tk.BooleanVar(value=False)
        show_pass_check = ttk.Checkbutton(
            self.main_frame, 
            text="Show password", 
            variable=self.show_password,
            command=self._toggle_password_visibility
        )
        show_pass_check.pack(anchor=tk.W, pady=5)
        
        # Remember me
        self.remember_me = tk.BooleanVar(value=True)
        remember_check = ttk.Checkbutton(
            self.main_frame, 
            text="Remember connection details", 
            variable=self.remember_me
        )
        remember_check.pack(anchor=tk.W, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        # Connect button
        connect_button = ttk.Button(
            buttons_frame, 
            text="Connect", 
            command=self._connect_to_mysql,
            style="Primary.TButton"
        )
        connect_button.pack(side=tk.RIGHT, padx=5)
        
        # Exit button
        exit_button = ttk.Button(
            buttons_frame, 
            text="Exit", 
            command=self.root.destroy
        )
        exit_button.pack(side=tk.RIGHT, padx=5)
        
        # Theme toggle button
        theme_button = ttk.Button(
            buttons_frame, 
            text="Toggle Theme", 
            command=lambda: self.config.toggle_theme(self.root)
        )
        theme_button.pack(side=tk.LEFT, padx=5)
        
        # Set focus to password field if username is already filled
        if self.user_var.get():
            pass_entry.focus_set()
        else:
            user_entry.focus_set()
        
        # Bind Enter key to connect
        self.root.bind("<Return>", lambda event: self._connect_to_mysql())
        
    def _toggle_password_visibility(self):
        """Toggle password visibility."""
        # Find the password entry widget
        for widget in self.main_frame.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Entry) and child.cget("show") == "*":
                        if self.show_password.get():
                            child.config(show="")
                        else:
                            child.config(show="*")
        
    def _connect_to_mysql(self):
        """Connect to MySQL server with the provided credentials."""
        host = self.host_var.get().strip()
        user = self.user_var.get().strip()
        password = self.pass_var.get()
        
        # Validate inputs
        if not host:
            messagebox.showerror("Error", "Please enter a host")
            return
        
        if not user:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        # Try to connect
        try:
            result = self.db_manager.connect_to_mysql(host, user, password)
            
            if isinstance(result, tuple) and not result[0]:
                messagebox.showerror("Connection Error", f"Failed to connect to MySQL: {result[1]}")
                return
                
            if not result:
                messagebox.showerror("Connection Error", "Failed to connect to MySQL")
                return
                
            # Save connection details if remember me is checked
            if self.remember_me.get():
                self.config.set("host", host)
                self.config.set("user", user)
            
            # Show success message
            messagebox.showinfo("Success", "Connected to MySQL successfully!")
            
            # Proceed to database selection
            self._open_database_selector()
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An error occurred: {e}")
            
    def _open_database_selector(self):
        """Open the database selector screen."""
        # Clear current window
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create database selector screen
        DatabaseSelector(self.root, self.main_frame, self.db_manager, self.config)