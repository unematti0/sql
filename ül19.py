import sqlite3

try:
    conn = sqlite3.connect('mattias_elmers.db')
    cursor = conn.cursor()
    print("Ühendus loodud")
    # Siia päringud

except sqlite3.Error as error:
    print("Tekkis viga andmebaasiga ühendamisel:", error)
finally:
    if conn:
        conn.close()