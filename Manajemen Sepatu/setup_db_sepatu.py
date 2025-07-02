import sqlite3
from konfigurasi import DB_PATH

def setup_database():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sepatu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                merk TEXT NOT NULL,
                kategori TEXT,
                ukuran REAL NOT NULL CHECK(ukuran > 0),
                tanggal_beli DATE NOT NULL,
                gambar TEXT
            );
        """)
        print("Tabel 'sepatu' dibuat/tersedia.")

if __name__ == "__main__":
    setup_database()
