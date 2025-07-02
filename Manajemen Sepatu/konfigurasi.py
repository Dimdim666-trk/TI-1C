import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NAMA_DB = 'koleksi_sepatu.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)

KATEGORI_SEPATU = ["FG", "SG", "AG", "TF", "IC", "Street"]
MERK_SEPATU = ["Nike", "Adidas", "Puma", "Mizuno", "Specs", "Lainnya"]
