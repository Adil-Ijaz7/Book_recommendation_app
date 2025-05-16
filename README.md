# 📚 Book Recommendation App

A Python desktop application that helps you discover, view, and save your favorite books using **CustomTkinter**. It fetches book data from the **Open Library** and **Google Books** APIs, and stores favorites in a **MySQL** database for future viewing.

---

## ✨ Features

- 🔍 Search for books by title or keyword
- 🖼️ View book cover, author, and a short description
- ❤️ Add books to a persistent **Favorites** list
- 📁 View all your saved books from the database
- 🌙 Beautiful dark-mode GUI using **CustomTkinter**
- 📡 Fetches data from Open Library & Google Books APIs
- 💾 Stores favorites locally using MySQL

---

## 🧩 Technologies Used

- **Python 3**
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Pillow (PIL)** – for image handling
- **Requests** – for API calls
- **MySQL** – for storing favorites
- `mysql-connector-python` – Python MySQL client



---

## 🏗️ Database Setup (`Appsql.txt`)

To get started with the backend:

1. Import `Appsql.txt` into your MySQL server:
   sql
   SOURCE path/to/Appsql.txt;


2. This will:

* Create a database `book_recommendation_db`
* Create a `favorites` table to store book info
* Create a user `book_user` with full privileges

3. Edit the connection settings in `App.py`:

   python
   host="localhost",
   user="book_user",        # or your username
   password="your_password",# replace with your MySQL password
   database="book_recommendation_db"
   
 ---
##💡 Future Features

* Add/remove favorites directly in UI
* User authentication
* Book rating system
* Multi-theme support

---

## 🛡️ License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.

---

## 🙋‍♂️ Author

**Adil Ijaz**
📧 [your.email@example.com](mailto:adilijaz227@gmail.com)
🔗 [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/Adil-Ijaz7)

---




