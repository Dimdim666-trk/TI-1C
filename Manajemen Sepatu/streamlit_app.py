import streamlit as st
import datetime
import os
from model import Sepatu
from manajer_sepatu import ManajerSepatu
from konfigurasi import KATEGORI_SEPATU, MERK_SEPATU

# Buat folder gambar jika belum ada
if not os.path.exists("gambar_sepatu"):
    os.makedirs("gambar_sepatu")

st.set_page_config("Koleksi Sepatu Bola", layout="wide")
st.title("👟 Manajemen Koleksi Sepatu Sepakbola")

manajer = ManajerSepatu()
tab1, tab2 = st.tabs(["➕ Tambah Sepatu", "📋 Daftar Koleksi"])

# ------------------------ TAB TAMBAH ------------------------
with tab1:
    st.subheader("Tambah Sepatu Baru")
    with st.form("form_sepatu", clear_on_submit=True):
        nama = st.text_input("Nama Sepatu", placeholder="Phantom GX, Predator, dll.")
        merk = st.selectbox("Merk", MERK_SEPATU)
        kategori = st.selectbox("Kategori", KATEGORI_SEPATU)
        ukuran = st.number_input("Ukuran (EU)", min_value=35.0, max_value=50.0, step=0.5)
        tanggal_beli = st.date_input("Tanggal Beli", value=datetime.date.today())
        uploaded_file = st.file_uploader("Upload Gambar Sepatu", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            st.image(uploaded_file, caption="Preview Gambar Sepatu", width=200)

        submit = st.form_submit_button("💾 Simpan")

        if submit:
            gambar_path = None
            if uploaded_file:
                nama_file = f"{nama.replace(' ', '_')}_{tanggal_beli}.png"
                gambar_path = os.path.join("gambar_sepatu", nama_file)
                with open(gambar_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            sepatu = Sepatu(nama, merk, kategori, ukuran, tanggal_beli, gambar=gambar_path)
            manajer.tambah_sepatu(sepatu)
            st.success("✅ Sepatu berhasil ditambahkan!")

# ------------------------ TAB DAFTAR ------------------------
with tab2:
    st.subheader("🔍 Filter Koleksi Sepatu")

    with st.form("filter_form"):
        filter_nama = st.text_input("Cari berdasarkan nama", value=st.session_state.get("filter_nama", ""))
        filter_merk = st.selectbox("Filter berdasarkan merk", ["Semua"] + MERK_SEPATU, index=(["Semua"] + MERK_SEPATU).index(st.session_state.get("filter_merk", "Semua")))
        filter_kategori = st.selectbox("Filter berdasarkan kategori", ["Semua"] + KATEGORI_SEPATU, index=(["Semua"] + KATEGORI_SEPATU).index(st.session_state.get("filter_kategori", "Semua")))

        colf1, colf2 = st.columns(2)
        apply = colf1.form_submit_button("🔎 Terapkan Filter")
        reset = colf2.form_submit_button("🔁 Reset Filter")

    if apply:
        st.session_state["filter_nama"] = filter_nama
        st.session_state["filter_merk"] = filter_merk
        st.session_state["filter_kategori"] = filter_kategori

    if reset:
        st.session_state.pop("filter_nama", None)
        st.session_state.pop("filter_merk", None)
        st.session_state.pop("filter_kategori", None)
        st.rerun()

    semua_sepatu = manajer.semua_sepatu()
    sepatu_list = [
        s for s in semua_sepatu
        if (st.session_state.get("filter_nama", "").lower() in s.nama.lower())
        and (st.session_state.get("filter_merk", "Semua") == "Semua" or s.merk == st.session_state.get("filter_merk"))
        and (st.session_state.get("filter_kategori", "Semua") == "Semua" or s.kategori == st.session_state.get("filter_kategori"))
    ]

    st.subheader("📋 Daftar Koleksi Sepatu")

    if not sepatu_list:
        st.info("Tidak ditemukan sepatu sesuai filter.")
    else:
        for sepatu in sepatu_list:
            with st.expander(f"{sepatu.nama} - {sepatu.merk} ({sepatu.kategori})"):
                col1, col2 = st.columns([1, 3])
                with col1:
                    if sepatu.gambar and isinstance(sepatu.gambar, str) and os.path.exists(sepatu.gambar):
                        st.image(sepatu.gambar, width=130)
                    else:
                        st.image("https://via.placeholder.com/130x130.png?text=No+Image", width=130)
                with col2:
                    st.write(f"**Ukuran:** {sepatu.ukuran} (EU)")
                    st.write(f"**Tanggal Beli:** {sepatu.tanggal_beli}")

                    col_a, col_b = st.columns(2)
                    if col_a.button("✏️ Edit", key=f"edit_{sepatu.id}"):
                        st.session_state["edit_id"] = sepatu.id
                    if col_b.button("🗑️ Hapus", key=f"hapus_{sepatu.id}"):
                        manajer.hapus_sepatu(sepatu.id)
                        if sepatu.gambar and os.path.exists(sepatu.gambar):
                            os.remove(sepatu.gambar)
                        st.success(f"Data sepatu '{sepatu.nama}' dihapus.")
                        st.rerun()

# ------------------------ FORM EDIT ------------------------
if "edit_id" in st.session_state:
    sepatu_ubah = next((s for s in semua_sepatu if s.id == st.session_state["edit_id"]), None)
    if sepatu_ubah:
        st.subheader("✏️ Edit Sepatu")
        with st.form("form_edit"):
            nama = st.text_input("Nama Sepatu", value=sepatu_ubah.nama)
            merk = st.selectbox("Merk", MERK_SEPATU, index=MERK_SEPATU.index(sepatu_ubah.merk))
            kategori = st.selectbox("Kategori", KATEGORI_SEPATU, index=KATEGORI_SEPATU.index(sepatu_ubah.kategori))
            ukuran = st.number_input("Ukuran (EU)", min_value=35.0, max_value=50.0, step=0.5, value=sepatu_ubah.ukuran)
            tanggal_beli = st.date_input("Tanggal Beli", value=sepatu_ubah.tanggal_beli)
            uploaded_file = st.file_uploader("Upload Gambar Baru (Opsional)", type=["jpg", "jpeg", "png"])

            if uploaded_file:
                st.image(uploaded_file, caption="Preview", width=200)

            simpan = st.form_submit_button("💾 Simpan Perubahan")

            if simpan:
                gambar_path = sepatu_ubah.gambar
                if uploaded_file:
                    if gambar_path and os.path.exists(gambar_path):
                        os.remove(gambar_path)
                    nama_file = f"{nama.replace(' ', '_')}_{tanggal_beli}_edit.png"
                    gambar_path = os.path.join("gambar_sepatu", nama_file)
                    with open(gambar_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                sepatu_baru = Sepatu(nama, merk, kategori, ukuran, tanggal_beli, gambar=gambar_path, id_sepatu=sepatu_ubah.id)
                manajer.update_sepatu(sepatu_baru)
                st.success("✅ Data berhasil diupdate.")
                del st.session_state["edit_id"]
                st.rerun()
