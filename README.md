# 🔐 MySecureDBManager

[![GitHub release](https://img.shields.io/github/v/release/jentimanatol/MySecureDBManagerGui)](https://github.com/jentimanatol/MySecureDBManagerGui/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> Created by **Anatolie Jentimir** — Designed for students, educators, and anyone learning secure MySQL database operations.

**MySecureDBManagerGui** is a secure and user-friendly command-line tool built in **Python** for managing a MySQL database with full **CRUD** support. Originally developed for an academic project at **Bunker Hill Community College**, it is now an open-source educational resource.

---  

## 🔽 Download

📦 Get the latest Windows executable here:  
➡️ **[Download v1.0 (.exe)](https://github.com/jentimanatol/MySecureDBManagerGui/releases/download/v1.0/MySecureDBManagerGui.exe)**

🕰️ Looking for source code or earlier versions?  
🔍 **[Browse all releases](https://github.com/jentimanatol/MySecureDBManagerGui/releases)**

---

## 📦 Features

- 🔒 Encrypted password handling with SHA-256
- 🧠 Intuitive CLI for database interaction
- 🗃️ Two relational tables:
  - `User` table with first name, last name, email, and access level
  - `Login` table linked by foreign key for secure credentials
- 🔑 Secure prompt for MySQL root password
- 🛠️ Full CRUD operations for both Users and Logins
- 🧩 Modular and beginner-friendly Python code

---

## 🗂️ Database Schema

### `User` Table

| Column       | Type     | Description                  |
|--------------|----------|------------------------------|
| `userId`     | INT      | Primary key, auto-increment  |
| `firstName`  | VARCHAR  | User's first name            |
| `lastName`   | VARCHAR  | User's last name             |
| `email`      | VARCHAR  | User's email address         |
| `accessLevel`| VARCHAR  | 'basic' or 'admin'           |

### `Login` Table

| Column       | Type     | Description                           |
|--------------|----------|---------------------------------------|
| `loginId`    | INT      | Primary key, auto-increment           |
| `userId`     | INT      | Foreign key to `User.userId`          |
| `username`   | VARCHAR  | Login username                        |
| `password`   | VARCHAR  | Encrypted password (SHA-256)          |

---

## 🧪 Perfect For

- Computer science students learning database design
- Educators teaching Python-MySQL integration
- Developers prototyping secure login systems
- Anyone practicing CRUD app development with encryption

---

## 🚀 How to Use

1. ✅ Install MySQL and Python 3.8+ on your system.
2. 📥 Download the `.exe` from the [latest release](https://github.com/jentimanatol/MySecureDBManagerGui/releases).
3. ▶️ Run `MySecureDBManagerGui.exe` or use the Python script directly:

```bash
pip install mysql-connector-python
python MySecureDBManagerGui.py
```

4. 🔐 Enter your MySQL root password when prompted.
5. 🗂️ Begin creating, reading, updating, and deleting records!

---

## 🎓 Academic Origin

Originally created as the final project for **CSC-225 – Introduction to Programming (Python)**  
**Bunker Hill Community College** – Spring 2025

---

## 👤 Author

**Anatolie Jentimir**  
Computer Science Student  
Bunker Hill Community College  

---

## 🛡 License

Licensed under the MIT License.  
Feel free to fork, use, and improve the code!

---

> 💬 _"Simple, secure, and built for students — that's MySecureDBManagerGui!"_
