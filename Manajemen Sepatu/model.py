import datetime

class Sepatu:
    def __init__(self, nama, merk, kategori, ukuran, tanggal_beli, gambar=None, id_sepatu=None):
        self.id = id_sepatu
        self.nama = nama
        self.merk = merk
        self.kategori = kategori
        self.ukuran = float(ukuran)
        self.tanggal_beli = tanggal_beli
        self.gambar = gambar

    def to_dict(self):
        return {
            "nama": self.nama,
            "merk": self.merk,
            "kategori": self.kategori,
            "ukuran": self.ukuran,
            "tanggal_beli": self.tanggal_beli.strftime("%Y-%m-%d"),
            "gambar": self.gambar
        }
