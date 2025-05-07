"""
User list view module for displaying and managing users.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class UserListView:
    """View for displaying and managing users."""
    
    def __init__(self, parent, db_manager, main_app):
        """Initialize user list view.
        
        Args:
            parent: Parent widget
            db_manager: Database manager instance
            main_app: Main application reference
        """
        self.parent = parent
        self.db_manager = db_manager
        self.main_app = main_app
        
        # Create widgets
        self._create_widgets()
        
        # Load users
        self._load_users()
    
    def _create_widgets(self):
        """Create view widgets."""
        # Create frame
        self.frame = ttk.Frame(self.parent, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create title with action buttons
        title_frame = ttk.Frame(self.frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="User Management", style="Title.TLabel")
        title_label.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            title_frame,
            text="Refresh",
            command=self._load_users
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        add_btn = ttk.Button(
            title_frame,
            text="Add New User",
            command=lambda: self.main_app._show_user_form(),
            style="Primary.TButton"
        )
        add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create search frame
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill=tk.X, pady=10)
        
        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter_users)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT)
        
        # Create treeview with scrollbar
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview columns
        columns = ("userId", "firstName", "lastName", "email", "accessLevel")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Define column headings
        self.tree.heading("userId", text="ID")
        self.tree.heading("firstName", text="First Name")
        self.tree.heading("lastName", text="Last Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("accessLevel", text="Access Level")
        
        # Define column widths
        self.tree.column("userId", width=50, anchor=tk.CENTER)
        self.tree.column("firstName", width=150)
        self.tree.column("lastName", width=150)
        self.tree.column("email", width=250)
        self.tree.column("accessLevel", width=100, anchor=tk.CENTER)
        
        # Add vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Add horizontal scrollbar
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        
        # Position scrollbars and treeview
        self.tree.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")
        
        # Configure grid weights for resizing
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Create action buttons frame
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        edit_btn = ttk.Button(
            action_frame,
            text="Edit User",
            command=self._edit_selected_user,
            style="Success.TButton"
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = ttk.Button(
            action_frame,
            text="Delete User",
            command=self._delete_selected_user,
            style="Danger.TButton"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Double-click to edit
        self.tree.bind("<Double-1>", lambda event: self._edit_selected_user())
        
        # Right-click context menu
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Edit User", command=self._edit_selected_user)
        self.context_menu.add_command(label="Delete User", command=self._delete_selected_user)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Refresh List", command=self._load_users)
        
        self.tree.bind("<Button-3>", self._show_context_menu)
    
    def _show_context_menu(self, event):
        """Show context menu on right-click.
        
        Args:
            event: Mouse event
        """
        # Select row under mouse
        iid = self.tree.identify_row(event.y)
        if iid:
            self.tree.selection_set(iid)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _load_users(self):
        """Load users from database into treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get users from database
        users = self.db_manager.select_all_users()
        
        # Add users to treeview
        for user in users:
            self.tree.insert("", "end", values=(
                user["userId"],
                user["firstName"],
                user["lastName"],
                user["email"],
                user["accessLevel"]
            ))
        
        # Update status
        self.main_app._update_status(f"Loaded {len(users)} users")
    
    def _filter_users(self, *args):
        """Filter users based on search text."""
        search_text = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all users
        users = self.db_manager.select_all_users()
        
        # Filter and add users to treeview
        filtered_count = 0
        for user in users:
            # Check if search text is in any field
            if (search_text in str(user["userId"]).lower() or
                search_text in user["firstName"].lower() or
                search_text in user["lastName"].lower() or
                search_text in user["email"].lower() or
                search_text in user["accessLevel"].lower()):
                
                self.tree.insert("", "end", values=(
                    user["userId"],
                    user["firstName"],
                    user["lastName"],
                    user["email"],
                    user["accessLevel"]
                ))
                filtered_count += 1
        
        # Update status
        if search_text:
            self.main_app._update_status(f"Found {filtered_count} users matching '{search_text}'")
        else:
            self.main_app._update_status(f"Loaded {filtered_count} users")
    
    def _get_selected_user_id(self):
        """Get the selected user ID.
        
        Returns:
            int: Selected user ID or None if no selection
        """
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Information", "Please select a user first")
            return None
        
        # Get user ID from the first column
        user_id = self.tree.item(selection[0], "values")[0]
        return int(user_id)
    
    def _edit_selected_user(self):
        """Edit the selected user."""
        user_id = self._get_selected_user_id()
        if user_id:
            self.main_app._show_user_form(user_id)
    
    def _delete_selected_user(self):
        """Delete the selected user."""
        user_id = self._get_selected_user_id()
        if user_id:
            # Confirm deletion
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user ID {user_id}?\nThis will also delete their login information."):
                # Delete user
                if self.db_manager.delete_user(user_id):
                    messagebox.showinfo("Success", f"User ID {user_id} deleted successfully")
                    self._load_users()
                else:
                    messagebox.showerror("Error", f"Failed to delete user ID {user_id}")