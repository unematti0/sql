import sqlite3

try:
    conn = sqlite3.connect('mattias_elmers.db')
    cursor = conn.cursor()
    print("Ühendus loodud")

    # Teostame päringu, et lugeda kõik andmed tabelist 'movies'

    


except sqlite3.Error as error:
    print("Tekkis viga andmebaasiga ühendamisel või päringu teostamisel:", error)
finally:
    if conn:
        conn.close()
        print("Ühendus suleti")

import tkinter as tk

# Loo Tkinteri aken
root = tk.Tk()
root.title("Filmi andmete sisestamine")

# Loo sildid ja sisestusväljad
labels = ["database", "tabeli nimi" ]
entries = {}

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(root, width=40)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[label] = entry

# Loo nupp andmete sisestamiseks
submit_button = tk.Button(root, text="Sisesta tabel")
submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)


# Näita Tkinteri akent
root.mainloop()