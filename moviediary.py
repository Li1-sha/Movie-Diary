import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import sqlite3

# Connect to the database or create a new one if it doesn't exist
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS movies (
                    title text,
                    genre text,
                    year integer,
                    rating real,
                    comment text
                )""")
conn.commit()


class LoginPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.check_credentials)
        self.login_button.pack()

    def check_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # In this example, we just check if the username and password are "admin" and "password"
        if username == "admin" and password == "password":
            self.destroy()
            HomePage()
        else:
            tk.messagebox.showerror("Error", "Invalid username or password.")


# Create the home page
class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Diary")
        self.geometry("600x200")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Movie Diary", font=("Futura", 42))
        title.pack()
        self.add_new_button = tk.Button(self, text="Add new", command=self.add_new_movie, padx=61,
                                        pady=6)
        self.add_new_button.place(x=335, y=85)

        self.view_all_button = tk.Button(self, text="View all", command=self.view_all_movies, padx=60,
                                         pady=6)
        self.view_all_button.place(x=65, y=120)

        self.library_button = tk.Button(self, text="Library", command=self.library, padx=62,
                                        pady=6)
        self.library_button.place(x=65, y=80)

    def add_new_movie(self):
        self.destroy()
        AddNewMoviePage()

    def view_all_movies(self):
        self.destroy()
        ViewAllMoviesPage()

    def library(self):
        self.destroy()
        LibraryPage()


# Create the page to add new movies
class AddNewMoviePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Add New Movie")
        self.geometry("400x250")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="Movie Name:")
        self.title_label.grid(row=1, column=0)
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=1, column=1)

        self.genre_label = tk.Label(self, text="Genre:")
        self.genre_label.grid(row=2, column=0)
        genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Musicals", "Mystery", "Romance",
                  "Science fiction", "Sports", "Thriller", "Western"]
        self.genre_var = tk.StringVar(self)

        self.genre_combobox = ttk.Combobox(self, textvariable=self.genre_var, values=genres)
        self.genre_combobox.grid(row=2, column=1)

        self.year_label = tk.Label(self, text="Year:")
        self.year_label.grid(row=3, column=0)
        self.year_entry = tk.Entry(self)
        self.year_entry.grid(row=3, column=1)

        self.rating_label = tk.Label(self, text="Rating (out of 5):")
        self.rating_label.grid(row=4, column=0)
        self.rating_scale = tk.Scale(self, from_=0, to=5, orient="horizontal")
        self.rating_scale.grid(row=4, column=1)

        self.comment_label = tk.Label(self, text="Comment:")
        self.comment_label.grid(row=5, column=0)
        self.comment_entry = tk.Entry(self)
        self.comment_entry.grid(row=5, column=1)

        self.save_button = tk.Button(self, text="Save", command=self.save_movie)
        self.save_button.grid(row=6, column=1)

        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.grid(row=7, column=1)

    def save_movie(self):
        title = self.title_entry.get()
        genre = self.genre_var.get()
        year = self.year_entry.get()
        rating = self.rating_scale.get()
        comment = self.comment_entry.get()

        cursor.execute("""INSERT INTO movies (title, genre, year, rating, comment)
                                  VALUES (?, ?, ?, ?, ?)""", (title, genre, year, rating, comment))
        conn.commit()

        tk.messagebox.showinfo("Success", "Movie saved successfully.")

    def go_back(self):
        self.destroy()
        HomePage()


# Create the page to view all movies
class ViewAllMoviesPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("View All Movies")
        self.geometry("800x350")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.movies_list = tk.Listbox(self)
        self.movies_list.pack()

        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
        for movie in movies:
            self.movies_list.insert(tk.END, movie)
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack()

    def go_back(self):
        self.destroy()
        HomePage()


# Create the page for the Library
class LibraryPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library")
        self.geometry("800x400")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()

        for movie in movies:
            tk.Button(self, text=movie[0], command=lambda movie=movie: self.view_movie(movie)).pack()

        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack()

    def view_movie(self, movie):
        ViewMoviePage(movie)

    def go_back(self):
        self.destroy()
        HomePage()


# Create the page to view a single movie
class ViewMoviePage(tk.Tk):
    def __init__(self, movie):
        super().__init__()
        self.movie = movie
        self.title(f"{self.movie[0]}")
        self.geometry("800x400")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Title: {self.movie[0]}").pack()
        tk.Label(self, text=f"Genre: {self.movie[1]}").pack()
        tk.Label(self, text=f"Year: {self.movie[2]}").pack()
        tk.Label(self, text=f"Rating: {self.movie[3]}").pack()
        tk.Label(self, text=f"Comment: {self.movie[4]}").pack()

        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack()

    def go_back(self):
        self.destroy()
        LibraryPage()


# Create the main menu
class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Diary")
        self.geometry("400x250")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "password":
            self.destroy()
            HomePage()
        else:
            tkinter.messagebox.messagebox.showerror("Error", "Invalid username or password")


# Show the login page
LoginPage().mainloop()
