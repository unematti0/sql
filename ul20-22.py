import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess


# Funktsioon, mis laadib andmed SQLite andmebaasist ja sisestab need Treeview tabelisse
def load_data_from_db(tree):
    # Loo ühendus SQLite andmebaasiga
    conn = sqlite3.connect("mattias_elmers.db")
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


# Funktsioon, mis laadib andmed SQLite andmebaasist ja sisestab need Treeview tabelisse
def load_data_from_db(tree, search_query=""):
    # Puhasta Treeview tabel enne uute andmete lisamist
    for item in tree.get_children():
        tree.delete(item)

    # Loo ühendus SQLite andmebaasiga
    conn = sqlite3.connect("mattias_elmers.db")
    cursor = conn.cursor()

    
    if search_query:
        cursor.execute(
            "SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users WHERE eesnimi LIKE ?",
            ("%" + search_query + "%",),
        )
    else:
        cursor.execute(
            "SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users"
        )

    rows = cursor.fetchall()

    # Lisa andmed tabelisse
    for row in rows:
        tree.insert(
            "", "end", values=row[1:], iid=row[0]
        )  # Määrake iid väärtuseks andmebaasi id

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


def lisa_andmeid():
    # Käivita ul19.py skript
    subprocess.Popen(["python", "ul19.py"], shell=True)


lisa_button = tk.Button(root, text="Lisa andmeid", command=lisa_andmeid)
lisa_button.pack(pady=10)


# ül21
# Funktsioon, mis uuendab andmed andmebaasis
def update_record(record_id, entries, window):
    # Koguge andmed sisestusväljadest
    eesnimi = entries["Eesnimi"].get()
    perenimi = entries["Perenimi"].get()
    email = entries["Email"].get()
    tel = entries["Telefon"].get()
    profiilipilt = entries["Profiilipilt"].get()

    # Andmete uuendamine andmebaasis
    conn = sqlite3.connect("mattias_elmers.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users
        SET eesnimi=?, perenimi=?, email=?, tel=?, profiilipilt=?
        WHERE id=?
    """,
        (eesnimi, perenimi, email, tel, profiilipilt, record_id),
    )
    conn.commit()
    conn.close()

    # Värskenda Treeview tabelit
    load_data_from_db(tree)

    # Sulge muutmise aken
    window.destroy()

    messagebox.showinfo("Salvestamine", "Andmed on edukalt uuendatud!")


# Funktsioon, mis avab muutmise akna
def open_update_window(record_id):
    # Loo uus aken
    update_window = tk.Toplevel(root)
    update_window.title("Muuda kasutaja andmeid")

    # Loo andmebaasi ühendus
    conn = sqlite3.connect("mattias_elmers.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT eesnimi, perenimi, email, tel, profiilipilt FROM users WHERE id=?",
        (record_id,),
    )
    record = cursor.fetchone()
    conn.close()

    # Kontrolli, kas rida leiti
    if record is None:
        messagebox.showerror("Viga", "Valitud rida ei leitud andmebaasist!")
        return

    
    labels = ["Eesnimi", "Perenimi", "Email", "Telefon", "Profiilipilt"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(
            row=i, column=0, padx=10, pady=5, sticky=tk.W
        )
        entry = tk.Entry(update_window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, record[i])
        entries[label] = entry

    # Salvestamise nupp
    save_button = tk.Button(
        update_window,
        text="Salvesta",
        command=lambda: update_record(record_id, entries, update_window),
    )
    save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)


def on_update():
    selected_item = tree.focus()  
    if not selected_item:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")
        return
    record_id = selected_item  
    open_update_window(record_id) 


# Lisa nupp muutmise jaoks
update_button = tk.Button(root, text="Uuenda", command=on_update)
update_button.pack(pady=10)
# ul21 lõpp

# ul22
def on_delete():
    selected_item = tree.selection()  # Võta valitud rida
    if selected_item:
        record_id = selected_item[0]  # iid (ID)
        confirm = messagebox.askyesno(
            "Kinnita kustutamine", "Kas oled kindel, et soovid selle rea kustutada?"
        )
        if confirm:
            try:
                # Loo andmebaasi ühendus
                conn = sqlite3.connect("mattias_elmers.db")
                cursor = conn.cursor()

                # Kustuta kirje
                cursor.execute("DELETE FROM users WHERE id=?", (record_id,))
                conn.commit()
                conn.close()

                # Värskenda Treeview tabelit
                load_data_from_db(tree)

                messagebox.showinfo("Edukalt kustutatud", "Rida on edukalt kustutatud!")
            except sqlite3.Error as e:
                messagebox.showerror("Viga", f"Andmebaasi viga: {e}")
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")


kustuta_button = tk.Button(root, text="Kustuta", command=on_delete)
kustuta_button.pack(pady=10)
# ul22 lõpp
# Loo tabel (Treeview) andmete kuvamiseks
tree = ttk.Treeview(
    frame,
    yscrollcommand=scrollbar.set,
    columns=("id", "eesnimi", "perenimi", "email", "tel", "profiilipilt"),
    show="headings",
)
tree.pack(fill=tk.BOTH, expand=True)

# Seosta kerimisriba tabeliga
scrollbar.config(command=tree.yview)

# Määra veergude pealkirjad ja laius
tree.heading("id", text="eesnimi")
tree.heading("eesnimi", text="eesnimi")
tree.heading("perenimi", text="perenimi")
tree.heading("email", text="gmail")
tree.heading("tel", text="telefoni number")
tree.heading("profiilipilt", text="pilt")

tree.column("id", width=50)
tree.column("eesnimi", width=150)
tree.column("perenimi", width=100)
tree.column("email", width=150)
tree.column("tel", width=100)
tree.column("profiilipilt", width=100)


# Lisa andmed tabelisse
load_data_from_db(tree)

root.mainloop()
