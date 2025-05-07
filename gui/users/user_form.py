"""
User form module for adding and editing users.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re


class UserForm:
    """Form for adding and editing users."""
    
    def __init__(self, parent, db_manager, main_app, user_id=None):
        """Initialize user form.
        
        Args:
            parent: Parent widget
            db_manager: Database manager instance
            main_app: Main application reference
            user_id: User ID to edit, or None for a new user
        """
        self.parent = parent
        self.db_manager = db_manager
        self.main_app = main_app
        self.user_id = user_id
        self.user_data = None
        
        # If editing, load user data
        if self.user_id:
            self.user_data = self.db_manager.select_user_by_id(self.user_id)
            if not self.user_data:
                messagebox.showerror("Error", f"User ID {self.user_id} not found")
                self.main_app._show_user_list()
                return
        
        # Create widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """Create form widgets."""
        # Create main frame
        self.frame = ttk.Frame(self.parent, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable container for the form
        canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        
        self.form_frame = ttk.Frame(canvas)
        self.form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create title
        if self.user_id:
            title_text = f"Edit User (ID: {self.user_id})"
        else:
            title_text = "Add New User"
            
        title_label = ttk.Label(self.form_frame, text=title_text, style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Create user information section
        user_frame = ttk.LabelFrame(self.form_frame, text="User Information", padding=10)
        user_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        
        # First name
        ttk.Label(user_frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.first_name_var = tk.StringVar(
            value=self.user_data["firstName"] if self.user_data else ""
        )
        ttk.Entry(user_frame, textvariable=self.first_name_var, width=30).grid(
            row=0, column=1, sticky="w", pady=5
        )
        
        # Last name
        ttk.Label(user_frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.last_name_var = tk.StringVar(
            value=self.user_data["lastName"] if self.user_data else ""
        )

        ttk.Entry(user_frame, textvariable=self.last_name_var, width=30).grid(
            row=1, column=1, sticky="w", pady=5
        )
        # Email
        ttk.Label(user_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar(
            value=self.user_data["email"] if self.user_data else ""
        )
        ttk.Entry(user_frame, textvariable=self.email_var, width=30).grid(
            row=2, column=1, sticky="w", pady=5
        )
        # Access level
        ttk.Label(user_frame, text="Access Level:").grid(row=3, column=0, sticky="w", pady=5)
        self.access_level_var = tk.StringVar(
            value=self.user_data["accessLevel"] if self.user_data else "user"
        )
        access_level_options = ["user", "admin"]
        self.access_level_combobox = ttk.Combobox(
            user_frame, textvariable=self.access_level_var, values=access_level_options, state="readonly"
        )
        self.access_level_combobox.grid(row=3, column=1, sticky="w", pady=5)
        self.access_level_combobox.current(
            access_level_options.index(self.access_level_var.get())
        )
        # Create buttons
        button_frame = ttk.Frame(self.form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        save_button = ttk.Button(
            button_frame,
            text="Save",
            command=self._save_user,
            style="Primary.TButton"
        )
        save_button.grid(row=0, column=0, padx=5)
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._cancel,
            style="Secondary.TButton"
        )
        cancel_button.grid(row=0, column=1, padx=5)
    def _save_user(self):

        """Save user data to the database."""
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        email = self.email_var.get().strip()
        access_level = self.access_level_var.get()
        
        # Validate input
        if not first_name or not last_name or not email:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Save user data
        if self.user_id:
            success = self.db_manager.update_user(
                self.user_id, first_name, last_name, email, access_level
            )
            action = "updated"
        else:
            success = self.db_manager.insert_user(
                first_name, last_name, email, access_level
            )
            action = "added"
        
        if success:
            messagebox.showinfo("Success", f"User successfully {action}")
            self.main_app._show_user_list()
        else:
            messagebox.showerror("Error", f"Failed to {action} user")



    
   