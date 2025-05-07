import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import mysql.connector
import os
from datetime import datetime

# Connect to MySQL database
def connect_to_mysql(password):
    host = "localhost"
    user = "root"

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database="BSelvarajLogins"
        )
        print("Connected to MySQL.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# GUI Class to encapsulate all UI logic
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management System")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Prevent window from being closed with the X button
        self.root.protocol("WM_DELETE_WINDOW", self.confirm_exit)
        
        # Get password with Tkinter dialog instead of getpass
        self.login_window()
        
    def login_window(self):
        # Create a login dialog
        login_frame = tk.Frame(self.root)
        login_frame.pack(padx=20, pady=20)
        
        tk.Label(login_frame, text="MySQL Password:").pack()
        
        # Password entry field
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(login_frame, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)
        password_entry.focus()
        
        # Login button
        tk.Button(login_frame, text="Connect", command=self.attempt_connection).pack(pady=10)
        
    def attempt_connection(self):
        password = self.password_var.get()
        self.conn = connect_to_mysql(password)
        
        if not self.conn:
            messagebox.showerror("Database Error", "Connection failed")
            return
            
        # Remove login frame and build main UI
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.cursor = self.conn.cursor()
        self.build_ui()

    def build_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # User management section
        tk.Label(button_frame, text="User Management", font=("Arial", 10, "bold")).pack(pady=(0, 5))
        tk.Button(button_frame, text="Add User", width=20, command=self.add_user).pack(pady=2)
        tk.Button(button_frame, text="View Users", width=20, command=self.view_users).pack(pady=2)
        tk.Button(button_frame, text="Update User Email", width=20, command=self.update_email).pack(pady=2)
        tk.Button(button_frame, text="Delete User", width=20, command=self.delete_user).pack(pady=2)
        
        # Login management section
        tk.Label(button_frame, text="Login Management", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        tk.Button(button_frame, text="Add Login", width=20, command=self.add_login).pack(pady=2)
        tk.Button(button_frame, text="View Logins", width=20, command=self.view_logins).pack(pady=2)
        tk.Button(button_frame, text="Delete Login", width=20, command=self.delete_login).pack(pady=2)
        
        # Database info section
        tk.Label(button_frame, text="Database Info", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        tk.Button(button_frame, text="View Tables", width=20, command=self.view_tables).pack(pady=2)
        tk.Button(button_frame, text="Database Stats", width=20, command=self.view_db_stats).pack(pady=2)
        
        # Output and utilities section
        tk.Label(button_frame, text="Utilities", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        tk.Button(button_frame, text="Save to File", width=20, command=self.save_to_file).pack(pady=2)
        tk.Button(button_frame, text="Clear Output", width=20, command=self.clear_output).pack(pady=2)
        tk.Button(button_frame, text="Exit", width=20, command=self.quit).pack(pady=(10, 2))
        
        # Right panel for output
        output_frame = tk.Frame(main_frame)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output area with scrollbar
        scroll = tk.Scrollbar(output_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.output = tk.Text(output_frame, height=20, width=60, yscrollcommand=scroll.set)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.output.yview)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def add_user(self):
        fname = simpledialog.askstring("Input", "First Name:")
        lname = simpledialog.askstring("Input", "Last Name:")
        email = simpledialog.askstring("Input", "Email:")
        access = simpledialog.askstring("Input", "Access Level (basic/admin):")
        try:
            self.cursor.callproc("AddUser", [fname, lname, email, access])
            self.conn.commit()
            messagebox.showinfo("Success", "User added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            self.conn.rollback()

    def add_login(self):
        user_id = simpledialog.askinteger("Input", "User ID (must exist):")
        username = simpledialog.askstring("Input", "Username:")
        password = simpledialog.askstring("Input", "Password:")
        try:
            self.cursor.callproc("AddLogin", [user_id, username, password.encode("utf-8")])
            self.conn.commit()
            messagebox.showinfo("Success", "Login added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            self.conn.rollback()

    def view_users(self):
        try:
            self.cursor.callproc("GetAllUsers")
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, "USER LIST\n")
            self.output.insert(tk.END, f"{'='*60}\n\n")
            self.output.insert(tk.END, f"{'ID':<5}{'First Name':<15}{'Last Name':<15}{'Email':<25}{'Access Level':<15}\n")
            self.output.insert(tk.END, f"{'-'*75}\n")
            
            count = 0
            for result in self.cursor.stored_results():
                rows = result.fetchall()
                count = len(rows)
                for row in rows:
                    # Format the row data nicely
                    user_id, fname, lname, email, access = row
                    self.output.insert(tk.END, f"{user_id:<5}{fname:<15}{lname:<15}{email:<25}{access:<15}\n")
            
            self.output.insert(tk.END, f"\nTotal Users: {count}\n")
            self.status_var.set(f"Loaded {count} users")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")

    def view_logins(self):
        try:
            self.cursor.callproc("GetAllLogins")
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, "LOGIN LIST\n")
            self.output.insert(tk.END, f"{'='*60}\n\n")
            self.output.insert(tk.END, f"{'ID':<5}{'User ID':<10}{'Username':<20}{'Created Date':<20}\n")
            self.output.insert(tk.END, f"{'-'*55}\n")
            
            count = 0
            for result in self.cursor.stored_results():
                rows = result.fetchall()
                count = len(rows)
                for row in rows:
                    # Format each row nicely without showing the password hash
                    login_id, user_id, username, _, created = row
                    self.output.insert(tk.END, f"{login_id:<5}{user_id:<10}{username:<20}{created}\n")
            
            self.output.insert(tk.END, f"\nTotal Logins: {count}\n")
            self.status_var.set(f"Loaded {count} logins")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")

    def update_email(self):
        user_id = simpledialog.askinteger("Input", "User ID:")
        new_email = simpledialog.askstring("Input", "New Email:")
        try:
            self.cursor.callproc("UpdateUserEmail", [user_id, new_email])
            self.conn.commit()
            messagebox.showinfo("Success", "Email updated.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            self.conn.rollback()

    def delete_user(self):
        user_id = simpledialog.askinteger("Input", "User ID to delete:")
        try:
            self.cursor.callproc("DeleteUser", [user_id])
            self.conn.commit()
            messagebox.showinfo("Success", "User deleted.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            self.conn.rollback()

    def delete_login(self):
        login_id = simpledialog.askinteger("Input", "Login ID to delete:")
        try:
            self.cursor.callproc("DeleteLogin", [login_id])
            self.conn.commit()
            messagebox.showinfo("Success", "Login deleted.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"MySQL Error: {err}")
            self.conn.rollback()

    def confirm_exit(self):
        """Confirm before exiting the application"""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.quit()
    
    def quit(self):
        """Close database connection and exit"""
        if hasattr(self, 'conn') and self.conn:
            self.cursor.close()
            self.conn.close()
        self.root.destroy()
        
    def clear_output(self):
        """Clear the output text area"""
        self.output.delete(1.0, tk.END)
        self.status_var.set("Output cleared")
        
    def save_to_file(self):
        """Save current output to a text file"""
        if not self.output.get(1.0, tk.END).strip():
            messagebox.showinfo("Info", "Nothing to save - output is empty")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Output As"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    content = self.output.get(1.0, tk.END)
                    f.write(content)
                self.status_var.set(f"Output saved to {os.path.basename(filename)}")
                messagebox.showinfo("Success", f"Output saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                
    def view_tables(self):
        """View all tables in the database"""
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"DATABASE: BSelvarajLogins\n")
            self.output.insert(tk.END, f"{'='*40}\n\n")
            self.output.insert(tk.END, "Tables:\n")
            
            for i, table in enumerate(tables, 1):
                self.output.insert(tk.END, f"{i}. {table[0]}\n")
                
                # Get table structure
                self.cursor.execute(f"DESCRIBE {table[0]}")
                columns = self.cursor.fetchall()
                self.output.insert(tk.END, f"\nStructure of {table[0]}:\n")
                self.output.insert(tk.END, f"{'Field':<20}{'Type':<20}{'Null':<10}{'Key':<10}{'Default':<15}{'Extra'}\n")
                self.output.insert(tk.END, f"{'-'*80}\n")
                
                for col in columns:
                    self.output.insert(tk.END, f"{col[0]:<20}{col[1]:<20}{col[2]:<10}{col[3]:<10}{col[4] if col[4] else 'NULL':<15}{col[5]}\n")
                
                self.output.insert(tk.END, f"\n{'='*40}\n\n")
            
            self.status_var.set(f"Found {len(tables)} tables")
        except mysql.connector.Error as err:
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"Error listing tables: {err}")
            self.status_var.set("Error")
            
    def view_db_stats(self):
        """View database statistics"""
        try:
            # Get database size
            self.cursor.execute("""
                SELECT 
                    table_schema as 'Database',
                    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as 'Size (MB)'
                FROM information_schema.tables
                WHERE table_schema = 'BSelvarajLogins'
                GROUP BY table_schema
            """)
            db_size = self.cursor.fetchone()
            
            # Get table counts
            self.cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = 'BSelvarajLogins'
            """)
            table_count = self.cursor.fetchone()[0]
            
            # Get user and login counts
            self.cursor.execute("SELECT COUNT(*) FROM Users")
            user_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM Logins")
            login_count = self.cursor.fetchone()[0]
            
            # Get newest user
            self.cursor.execute("""
                SELECT CONCAT(FirstName, ' ', LastName), Email
                FROM Users ORDER BY UserID DESC LIMIT 1
            """)
            newest_user = self.cursor.fetchone()
            
            # Display results
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"DATABASE STATISTICS\n")
            self.output.insert(tk.END, f"{'='*40}\n\n")
            self.output.insert(tk.END, f"Database Name: BSelvarajLogins\n")
            self.output.insert(tk.END, f"Database Size: {db_size[1]} MB\n")
            self.output.insert(tk.END, f"Number of Tables: {table_count}\n")
            self.output.insert(tk.END, f"Number of Users: {user_count}\n")
            self.output.insert(tk.END, f"Number of Logins: {login_count}\n")
            self.output.insert(tk.END, f"Newest User: {newest_user[0]} ({newest_user[1]})\n")
            self.output.insert(tk.END, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            self.status_var.set("Database statistics loaded")
        except mysql.connector.Error as err:
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, f"Error getting database statistics: {err}")
            self.status_var.set("Error")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()