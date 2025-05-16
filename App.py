import customtkinter as ctk
import requests
from PIL import Image
from io import BytesIO
import mysql.connector
from mysql.connector import Error

ctk.set_appearance_mode("Dark")

class BookRecommendationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db_connection = self.create_db_connection()
        self.create_favorites_table()

        self.title("Book Recommendation App")
        self.geometry("1000x750")
        self.resizable(False, False)

        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E2E")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.header_label = ctk.CTkLabel(
            self.content_frame, text="Discover Your Next Favorite Book",
            font=("Roboto", 30, "bold"), text_color="#A6E3A1"
        )
        self.header_label.pack(pady=20)

        self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="#29293d", corner_radius=10)
        self.search_frame.pack(fill="x", pady=15, padx=20)

        self.search_entry = ctk.CTkEntry(
            self.search_frame, placeholder_text="Search for a book...", width=600, height=40,
            fg_color="#1E1E2E", text_color="#FFFFFF"
        )
        self.search_entry.pack(side="left", padx=10, pady=10)

        self.search_button = ctk.CTkButton(
            self.search_frame, text="Search", command=self.search_books, width=100, fg_color="#7F57F6"
        )
        self.search_button.pack(side="left", padx=5)

        self.view_favorites_button = ctk.CTkButton(
            self.search_frame, text="View Favorites", command=self.view_favorites, width=120, fg_color="#F75C7A"
        )
        self.view_favorites_button.pack(side="left", padx=5)

        self.recommendations_label = ctk.CTkLabel(
            self.content_frame, text="Recommended Books", font=("Roboto", 22, "bold"), text_color="#A6E3A1"
        )
        self.recommendations_label.pack(pady=15)

        self.recommendations_frame = ctk.CTkScrollableFrame(
            self.content_frame, width=800, height=500, corner_radius=10, fg_color="#29293d"
        )
        self.recommendations_frame.pack(fill="both", expand=True, pady=15, padx=20)

        self.footer_label = ctk.CTkLabel(
            self.content_frame, text="Powered by Open Library & Google Books APIs",
            font=("Roboto", 14), text_color="#89DCEB"
        )
        self.footer_label.pack(pady=10)

        self.load_home_screen()

    def create_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",       # ← Update your username
                password="714277", # ← Update your password
                database="book_recommendation_db"
            )
            print("MySQL Database connection successful")
            return connection
        except Error as e:
            print(f"Error: '{e}'")
            return None

    def create_favorites_table(self):
        if self.db_connection:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS favorites (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author VARCHAR(255),
                        cover_id VARCHAR(50),
                        description TEXT,
                        olid VARCHAR(50)
                    )
                """)
                self.db_connection.commit()
            except Error as e:
                print(f"Error: '{e}'")

    def fetch_books(self, query):
        url = f"https://openlibrary.org/search.json?q={query}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("docs", [])
        return []

    def fetch_book_description(self, title, author):
        try:
            query = f"{title} {author}"
            url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "items" in data:
                    volume_info = data["items"][0].get("volumeInfo", {})
                    return volume_info.get("description", "No description available")
        except:
            pass
        return "No description available"

    def display_recommendations(self, books):
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()

        for book in books[:8]:
            title = book.get("title", "Unknown Title")
            author = ", ".join(book.get("author_name", ["Unknown Author"]))
            cover_id = book.get("cover_i", None)
            olid = book.get("key", "").split("/")[-1] if "key" in book else None
            description = self.fetch_book_description(title, author)

            book_card = ctk.CTkFrame(self.recommendations_frame, corner_radius=10, fg_color="#1E1E2E")
            book_card.pack(fill="x", pady=10, padx=10)

            # Left image
            left_frame = ctk.CTkFrame(book_card, fg_color="transparent")
            left_frame.pack(side="left", fill="y", padx=10)

            if cover_id:
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                response = requests.get(cover_url)
                if response.status_code == 200:
                    cover_image = Image.open(BytesIO(response.content))
                    cover_image = cover_image.resize((80, 120))
                    cover_photo = ctk.CTkImage(cover_image, size=(80, 120))

                    cover_label = ctk.CTkLabel(left_frame, image=cover_photo, text="")
                    cover_label.image = cover_photo
                    cover_label.pack()

            # Middle info
            info_frame = ctk.CTkFrame(book_card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10)

            title_label = ctk.CTkLabel(info_frame, text=title, font=("Roboto", 16, "bold"), text_color="#A6E3A1")
            title_label.pack(anchor="w")

            author_label = ctk.CTkLabel(info_frame, text=f"by {author}", font=("Roboto", 14), text_color="#D9E0EE")
            author_label.pack(anchor="w")

            short_desc = (description[:150] + '...') if len(description) > 150 else description
            desc_label = ctk.CTkLabel(info_frame, text=short_desc, font=("Roboto", 12), text_color="#D9E0EE", wraplength=500)
            desc_label.pack(anchor="w", pady=5)

            # Right actions
            action_frame = ctk.CTkFrame(book_card, fg_color="transparent")
            action_frame.pack(side="right", fill="y", padx=10)

            view_button = ctk.CTkButton(
                action_frame, text="🔍 View", width=90, fg_color="#89DCEB",
                command=lambda b=book, d=description: self.open_book_card(b, d)
            )
            view_button.pack(pady=5)

            fav_button = ctk.CTkButton(
                action_frame, text="❤ Favorite", width=90, fg_color="#F75C7A",
                command=lambda b=book: self.add_to_favorites(b)
            )
            fav_button.pack(pady=5)

    def open_book_card(self, book, description):
        title = book.get("title", "Unknown Title")
        author = ", ".join(book.get("author_name", ["Unknown Author"]))
        cover_id = book.get("cover_i", None)

        popup = ctk.CTkToplevel(self)
        popup.title("Book Details")
        popup.geometry("500x600")

        frame = ctk.CTkFrame(popup, fg_color="#1E1E2E", corner_radius=10)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        if cover_id:
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            response = requests.get(cover_url)
            if response.status_code == 200:
                cover_image = Image.open(BytesIO(response.content)).resize((150, 220))
                cover_photo = ctk.CTkImage(cover_image, size=(150, 220))
                img_label = ctk.CTkLabel(frame, image=cover_photo, text="")
                img_label.image = cover_photo
                img_label.pack(pady=10)

        ctk.CTkLabel(frame, text=title, font=("Roboto", 20, "bold"), text_color="#A6E3A1", wraplength=450).pack(pady=5)
        ctk.CTkLabel(frame, text=f"by {author}", font=("Roboto", 16), text_color="#D9E0EE").pack(pady=5)

        desc_widget = ctk.CTkTextbox(frame, width=450, height=300, fg_color="#2E2E3E", text_color="#FFFFFF")
        desc_widget.insert("0.0", description or "No description available.")
        desc_widget.configure(state="disabled")
        desc_widget.pack(pady=10)

    def add_to_favorites(self, book):
        if not self.db_connection:
            print("No database connection")
            return

        title = book.get("title", "Unknown Title")
        author = ", ".join(book.get("author_name", ["Unknown Author"]))
        cover_id = book.get("cover_i", None)
        olid = book.get("key", "").split("/")[-1] if "key" in book else None
        description = self.fetch_book_description(title, author)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM favorites WHERE title = %s AND author = %s", (title, author))
            if cursor.fetchone():
                print("Book already in favorites")
                return

            cursor.execute("""
                INSERT INTO favorites (title, author, cover_id, description, olid)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, author, cover_id, description, olid))
            self.db_connection.commit()
            print("Book added to favorites")
        except Error as e:
            print(f"Error: '{e}'")

    def view_favorites(self):
        if not self.db_connection:
            print("No database connection")
            return

        try:
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM favorites")
            favorites = cursor.fetchall()

            if not favorites:
                for widget in self.recommendations_frame.winfo_children():
                    widget.destroy()

                no_fav_label = ctk.CTkLabel(
                    self.recommendations_frame, text="No favorites yet!",
                    font=("Roboto", 16), text_color="#D9E0EE"
                )
                no_fav_label.pack(pady=50)
            else:
                formatted = []
                for fav in favorites:
                    formatted.append({
                        "title": fav["title"],
                        "author_name": [fav["author"]] if fav["author"] else ["Unknown Author"],
                        "cover_i": fav["cover_id"],
                        "key": f"/works/{fav['olid']}" if fav["olid"] else None,
                    })
                self.display_recommendations(formatted)

        except Error as e:
            print(f"Error: '{e}'")

    def search_books(self):
        query = self.search_entry.get()
        if query:
            books = self.fetch_books(query)
            self.display_recommendations(books)

    def load_home_screen(self):
        books = self.fetch_books("bestsellers")
        self.display_recommendations(books)

    def __del__(self):
        if hasattr(self, 'db_connection') and self.db_connection:
            self.db_connection.close()

if __name__ == "__main__":
    app = BookRecommendationApp()
    app.mainloop()
