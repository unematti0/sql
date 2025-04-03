import tkinter as tk
from tkinter import ttk
import sqlite3

#Funktsioon, mis laadib andmed SQLite andmebaasist ja sisestab need Treeview tabelisse
def load_data_from_db(tree):
    # Loo ühendus SQLite andmebaasiga
    conn = sqlite3.connect('mattias_elmers.db')
    cursor = conn.cursor()

    # Tee päring andmebaasist andmete toomiseks
    cursor.execute("SELECT eesnimi, perenimi, email, tel, profiilipilt FROM users")
    rows = cursor.fetchall()

    # Lisa andmed tabelisse
    for row in rows:
        tree.insert("", "end", values=row)

    # Sulge ühendus andmebaasiga
    conn.close()

root = tk.Tk()
root.title("kasutajad")


# Loo raam kerimisribaga
frame = tk.Frame(root)
frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# Loo otsinguväli ja nupp


#Funktsioon, mis laadib andmed SQLite andmebaasist ja sisestab need Treeview tabelisse
def load_data_from_db(tree, search_query=""):
    # Puhasta Treeview tabel enne uute andmete lisamist
    for item in tree.get_children():
        tree.delete(item)

    # Loo ühendus SQLite andmebaasiga
    conn = sqlite3.connect('mattias_elmers.db')
    cursor = conn.cursor()

    # Tee päring andmebaasist andmete toomiseks
    if search_query:
        cursor.execute("SELECT title, director, release_year, genre, duration, rating, language, country, description FROM movies WHERE title LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT title, director, release_year, genre, duration, rating, language, country, description FROM movies")

    rows = cursor.fetchall()

    # Lisa andmed tabelisse
    for row in rows:
        tree.insert("", "end", values=row)

    # Sulge ühendus andmebaasiga
    conn.close()


def on_search():
    search_query = search_entry.get()
    load_data_from_db(tree, search_query)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Otsi filmi pealkirja järgi:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(search_frame, text="Otsi", command=on_search)
search_button.pack(side=tk.LEFT)


# Loo tabel (Treeview) andmete kuvamiseks
tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, columns=("eesnimi", "perenimi", "email", "tel", "profiilipilt"), show="headings")
tree.pack(fill=tk.BOTH, expand=True)

# Seosta kerimisriba tabeliga
scrollbar.config(command=tree.yview)

# Määra veergude pealkirjad ja laius
tree.heading("eesnimi", text="eesnimi")
tree.heading("perenimi", text="perenimi")
tree.heading("email", text="gmail")
tree.heading("tel", text="telefoni number")
tree.heading("profiilipilt", text="pilt")


tree.column("eesnimi", width=150)
tree.column("perenimi", width=100)
tree.column("email", width=60)
tree.column("tel", width=100)
tree.column("profiilipilt", width=60)


# Lisa andmed tabelisse
load_data_from_db(tree)

root.mainloop()