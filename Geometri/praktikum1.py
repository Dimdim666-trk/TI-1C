import cv2
import time

# 1. Inisialisasi Kamera
# Coba buka kamera dengan index 0 (kamera default)
cap = cv2.VideoCapture(0)

# Periksa apakah kamera berhasil dibuka
if not cap.isOpened():
    # Jika gagal, tampilkan pesan error sesuai anjuran di langkah praktikum
    raise RuntimeError("Kamera tidak bisa dibuka. Coba ganti index menjadi 1 atau 2 pada cv2.VideoCapture(0).")

# 2. Inisialisasi Penghitung FPS
frames = 0
t0 = time.time()

# 3. Loop Utama untuk Membaca Frame
while True:
    # Baca frame dari kamera
    ok, frame = cap.read()

    # Jika gagal membaca frame (misalnya, kamera terputus), keluar dari loop
    if not ok:
        break

    # Hitung FPS (Frame Per Second)
    frames += 1
    if time.time() - t0 >= 1.0:
        # Update judul jendela dengan nilai FPS
        # Gunakan 'int(frames)' untuk memastikan FPS ditampilkan sebagai bilangan bulat
        cv2.setWindowTitle("Preview", f"Preview (FPS ~ {int(frames)})")
        # Reset penghitung
        frames = 0
        t0 = time.time()

    # Tampilkan frame
    cv2.imshow("Preview", frame)

    # Logika Keluar: Tekan tombol 'q' untuk keluar
    # cv2.waitKey(1) menunggu 1ms untuk input keyboard
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 4. Cleanup (Pembersihan)
# Matikan koneksi ke kamera
cap.release()
# Tutup semua jendela OpenCV yang terbuka
cv2.destroyAllWindows()