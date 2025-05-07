import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector
import getpass

# Connect to MySQL database
def connect_to_mysql():
    host = "localhost"
    user = "root"
    password = getpass.getpass("Enter MySQL root password: ")

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
        self.conn = connect_to_mysql()
        if not self.conn:
            messagebox.showerror("Database Error", "Connection failed")
            root.destroy()
            return
        self.cursor = self.conn.cursor()
        self.build_ui()

    def build_ui(self):
        # Buttons for actions
        tk.Button(self.root, text="Add User", width=20, command=self.add_user).pack(pady=5)
        tk.Button(self.root, text="Add Login", width=20, command=self.add_login).pack(pady=5)
        tk.Button(self.root, text="View Users", width=20, command=self.view_users).pack(pady=5)
        tk.Button(self.root, text="View Logins", width=20, command=self.view_logins).pack(pady=5)
        tk.Button(self.root, text="Update User Email", width=20, command=self.update_email).pack(pady=5)
        tk.Button(self.root, text="Delete User", width=20, command=self.delete_user).pack(pady=5)
        tk.Button(self.root, text="Delete Login", width=20, command=self.delete_login).pack(pady=5)
        tk.Button(self.root, text="Exit", width=20, command=self.quit).pack(pady=5)

        self.output = tk.Text(self.root, height=15, width=60)
        self.output.pack(pady=10)

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
        self.cursor.callproc("GetAllUsers")
        self.output.delete(1.0, tk.END)
        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.output.insert(tk.END, f"{row}\n")

    def view_logins(self):
        self.cursor.callproc("GetAllLogins")
        self.output.delete(1.0, tk.END)
        for result in self.cursor.stored_results():
            for row in result.fetchall():
                self.output.insert(tk.END, f"{row}\n")

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

    def quit(self):
        self.cursor.close()
        self.conn.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
