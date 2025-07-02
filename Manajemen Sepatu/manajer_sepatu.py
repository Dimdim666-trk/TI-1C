from model import Sepatu
import database

class ManajerSepatu:
    def tambah_sepatu(self, sepatu: Sepatu):
        sql = """
        INSERT INTO sepatu (nama, merk, kategori, ukuran, tanggal_beli, gambar)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return database.execute_query(sql, (
            sepatu.nama, sepatu.merk, sepatu.kategori,
            sepatu.ukuran, sepatu.tanggal_beli.strftime("%Y-%m-%d"),
            sepatu.gambar
        ))

    def semua_sepatu(self):
        rows = database.fetch_all("SELECT * FROM sepatu ORDER BY tanggal_beli DESC")
        return [
            Sepatu(row["nama"], row["merk"], row["kategori"], row["ukuran"], row["tanggal_beli"], row["gambar"], row["id"])
            for row in rows
        ]

    def dataframe_sepatu(self):
        return database.fetch_dataframe("SELECT * FROM sepatu ORDER BY tanggal_beli DESC")

    def update_sepatu(self, sepatu: Sepatu):
        sql = """
        UPDATE sepatu
        SET nama=?, merk=?, kategori=?, ukuran=?, tanggal_beli=?, gambar=?
        WHERE id=?
        """
        return database.execute_query(sql, (
            sepatu.nama, sepatu.merk, sepatu.kategori,
            sepatu.ukuran, sepatu.tanggal_beli.strftime("%Y-%m-%d"),
            sepatu.gambar, sepatu.id
        ))

    def hapus_sepatu(self, id_sepatu):
        sql = "DELETE FROM sepatu WHERE id=?"
        return database.execute_query(sql, (id_sepatu,))
