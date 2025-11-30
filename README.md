# 📚 Book Recommendation App

A modern Python desktop application that helps you discover, preview, and save your favorite books using a clean dark-themed GUI built with **CustomTkinter**. It aggregates book information from the **Open Library** and **Google Books** APIs and persists your favorites in a local **MySQL** database.

> Discover books fast. Save what you love. Come back later.

---

## 🔥 Key Features

| Feature | Description |
|---------|-------------|
| 🔍 Search | Enter a title or keyword; results combine multiple public sources |
| 🖼️ Rich Preview | Cover image, title, authors, published year, short description |
| ❤️ Favorites | Persist selected books locally, even after you close the app |
| 📁 Library View | Browse all saved favorite entries with pagination (if implemented) |
| 🔄 Multi-Source Fetch | Falls back between APIs when data fields are missing |
| 🌙 Dark UI | Consistent dark mode via CustomTkinter styling |
| 🧹 Data Normalization | Cleans/merges responses (e.g., authors list formatting) |
| 💾 Local Storage | Uses MySQL for durability and structured querying |

---

## 🧩 Technology Stack

- **Python 3.x**
- **CustomTkinter** – Themable Tkinter UI components
- **Pillow (PIL)** – Image processing for book covers
- **Requests** – HTTP requests to external APIs
- **MySQL** – Persistent storage for favorites
- `mysql-connector-python` – Database connectivity
- (Optional) **dotenv** – For securing credentials in a `.env` file

---

## 🖼️ Screenshots (Optional)

Add screenshots/gifs here for better visual appeal:

| Search View | Favorite Stored | List View |
|-------------|-----------------|-----------|
| ![search](assets/search.png) | ![favorite](assets/favorite.png) | ![list](assets/list.png) |

> If you don’t have an `assets/` directory yet, create one and place images there.

---

## 🏗️ Architecture Overview

```
App.py
├── UI initialization (CustomTkinter root)
├── Search input / buttons
├── API handler calls
├── Image fetch & resize (Pillow)
├── Favorites save/retrieve (MySQL)
└── Error / empty-state handling
```

**Data Flow**  
1. User enters a search term.  
2. App queries Open Library API; optionally augments with Google Books if fields are missing.  
3. Response normalized (title, authors, description, cover URL).  
4. UI displays book cards (image + metadata).  
5. User clicks "Add to Favorites" → INSERT into MySQL `favorites` table.  
6. "View Favorites" pulls all rows and renders them.

---

## 🗄️ Database Setup

The repository includes `Appsql.txt` which bootstraps your database.

### 1. Import Schema

From MySQL CLI:
```sql
SOURCE /absolute/path/to/Appsql.txt;
```

This creates:
- Database: `book_recommendation_db`
- Table: `favorites`
- User: `book_user` (with privileges)

### 2. Table Structure (Sample)

```sql
CREATE TABLE favorites (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  authors VARCHAR(255),
  description TEXT,
  cover_url VARCHAR(500),
  source VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

(Adjust columns/types if different in `Appsql.txt`.)

### 3. Connection Configuration

In `App.py` (example):
```python
db_config = {
    "host": "localhost",
    "user": "book_user",
    "password": "your_password",           # Replace
    "database": "book_recommendation_db"
}
```

### 4. (Optional) Use Environment Variables

Create a `.env` file:
```
DB_HOST=localhost
DB_USER=book_user
DB_PASS=your_password
DB_NAME=book_recommendation_db
```

Then in code:
```python
from dotenv import load_dotenv
import os
load_dotenv()
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}
```

> Add `.env` to `.gitignore` to avoid committing secrets.

---

## 🌐 External APIs

| API | Endpoint Example | Usage |
|-----|------------------|-------|
| Open Library | `https://openlibrary.org/search.json?q=QUERY` | Initial book search |
| Google Books | `https://www.googleapis.com/books/v1/volumes?q=QUERY` | Supplements missing data |

You can implement graceful fallback logic:
```python
def fetch_book_data(query):
    data = fetch_open_library(query)
    if not data or missing_fields(data):
        data = merge_data(data, fetch_google_books(query))
    return normalize(data)
```

---

## ✅ Installation & Setup

1. Clone repository:
   ```bash
   git clone https://github.com/Adil-Ijaz7/Book_recommendation_app.git
   cd Book_recommendation_app
   ```

2. Create & activate virtual environment (recommended):
   ```bash
   python -m venv .venv
   # Linux/macOS:
   source .venv/bin/activate
   # Windows:
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If no `requirements.txt` yet, generate one:
   ```bash
   pip freeze > requirements.txt
   ```

4. Set up MySQL (see Database Setup above).

5. Run the app:
   ```bash
   python App.py
   ```

---

## ⚙️ Configuration

| Item | Purpose | Where |
|------|---------|-------|
| DB credentials | Connect to MySQL | `App.py` or `.env` |
| API Keys | (If later using Google Books API key) | `.env` |
| Image Cache | (Optional future optimization) | `cache/` directory |

---

## 🚨 Error Handling & Edge Cases

| Case | Strategy |
|------|----------|
| No results | Display a user-friendly "No books found" message |
| Missing cover | Show a placeholder image |
| API timeout | Retry once; display toast/dialog |
| DB connection failure | Alert user, disable "Add to Favorites" |
| Duplicate favorite | Prevent duplicate INSERT or allow but show notice |

---

## 🧪 Potential Enhancements (Roadmap)

| Status | Item | Description |
|--------|------|-------------|
| Planned | Pagination | Efficient browsing of large favorites list |
| Planned | Export | Allow exporting favorites to CSV/JSON |
| Planned | Tags | User-defined tags/categories for favorites |
| Future  | Recommendation Engine | Simple content-based filtering |
| Future  | User Profiles | Multi-user favorites separation |
| Future  | Async Requests | Speed up API responsiveness |
| Future  | Cover Caching | Reduce repeated network calls |

Add a GitHub Issues label like `enhancement` to track these.

---

## 🤝 Contributing

1. Fork the project
2. Create a feature branch:  
   `git checkout -b feat/meaningful-name`
3. Commit changes:  
   `git commit -m "Add: short description of feature"`
4. Push branch:  
   `git push origin feat/meaningful-name`
5. Open a Pull Request

Please follow consistent code style and run tests (if/when added).

---

## 🧪 Testing (Optional Section)

If you introduce tests later:
```bash
pytest -v
```
Structure suggestion:
```
tests/
  test_api_fetch.py
  test_db_integration.py
  test_normalization.py
```

---

## 📂 Project Structure (Example)

```
Book_recommendation_app/
├── App.py
├── README.md
├── Appsql.txt
├── requirements.txt
├── assets/              # (screenshots, icons)
├── utils/               # (future: helpers, API adapters)
└── tests/               # (future: test modules)
```

---

## 📄 License

Licensed under the **MIT License**. See [LICENSE](LICENSE) (add file if missing).

---

## 🙋‍♂️ Author

**Adil Ijaz**  
📧 [Email](mailto:adilijaz227@gmail.com)  
🔗 [LinkedIn](https://linkedin.com/in/yourprofile)  
🐙 [GitHub (Adil-Ijaz7)](https://github.com/Adil-Ijaz7)

---

## 💡 Acknowledgements

- [Open Library](https://openlibrary.org/) – Open book data
- [Google Books](https://developers.google.com/books) – Supplemental metadata
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) – Modern UI components
- Early adopters & testers (add names here)

---

## 📌 Badges (Optional)

You can add badges at the top for quick metadata:

```
![Python Version](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
```

---

> If you’d like, we can also create a `CONTRIBUTING.md`, `LICENSE`, or add a `requirements.txt` based on current imports.

Happy coding! 🚀
