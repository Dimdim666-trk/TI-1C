import cv2
import numpy as np
from cvzone.FaceMeshModule import FaceMeshDetector

# Indeks FaceMesh untuk landmark mata kiri (berdasarkan MediaPipe)
# Vertikal: atas (159), bawah (145)
# Horizontal: kiri/luar (33), kanan/dalam (133)
L_TOP, L_BOTTOM, L_LEFT, L_RIGHT = 159, 145, 33, 133

# Fungsi untuk menghitung jarak Euclidean antara dua titik
def dist(p1, p2):
    """Menghitung jarak Euclidean antara dua titik (p1 dan p2)."""
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Inisialisasi Kamera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Kamera tidak bisa dibuka.")

# Inisialisasi objek FaceMeshDetector
# staticMode: False (deteksi pada setiap frame)
# maxFaces: 2 (maksimum dua wajah)
# minDetectionCon: 0.5 (ambang kepercayaan deteksi)
detector = FaceMeshDetector(
    staticMode=False,
    maxFaces=2,
    minDetectionCon=0.5,
    minTrackCon=0.5
)

# Variabel untuk menghitung kedipan
blink_count = 0
closed_frames = 0
CLOSED_FRAMES_THRESHOLD = 3  # Jumlah frame berturut-turut mata harus tertutup
EYE_AR_THRESHOLD = 0.20      # Ambang batas EAR untuk dianggap mata tertutup
is_closed = False            # Status kedipan saat ini

# Loop Utama
while True:
    # 1. Baca Frame
    ok, img = cap.read()
    if not ok:
        break

    # 2. Deteksi Face Mesh
    img, faces = detector.findFaceMesh(img, draw=True)

    # 3. Proses Wajah yang Terdeteksi
    if faces:
        face = faces[0]  # Ambil wajah pertama (list 468 landmark [x, y, z])

        # Hitung Jarak (Jarak vertikal vs Jarak horizontal)
        v = dist(face[L_TOP], face[L_BOTTOM])  # Jarak Vertikal (tinggi mata)
        h = dist(face[L_LEFT], face[L_RIGHT])  # Jarak Horizontal (lebar mata)
        
        # Hitung Eye Aspect Ratio (EAR)
        # Tambahkan 1e-8 untuk menghindari pembagian dengan nol
        ear = v / (h + 1e-8)

        # Tampilkan nilai EAR
        cv2.putText(img, f"EAR(L): {ear:.3f}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        # 4. Logika Penghitungan Kedipan (Blink Counter)
        if ear < EYE_AR_THRESHOLD:
            # Mata tertutup
            closed_frames += 1

            # Cek apakah mata telah tertutup cukup lama DAN belum dihitung
            if closed_frames >= CLOSED_FRAMES_THRESHOLD and not is_closed:
                blink_count += 1
                is_closed = True  # Tandai sebagai sudah dihitung (kedipan tunggal)
        else:
            # Mata terbuka
            closed_frames = 0
            is_closed = False

        # Tampilkan jumlah kedipan pada frame
        cv2.putText(img, f"Blink: {blink_count}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # 5. Tampilkan Frame dan Keluar
    cv2.imshow("FaceMesh + EAR", img)
    
    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Pembersihan (Cleanup)
cap.release()
cv2.destroyAllWindows()