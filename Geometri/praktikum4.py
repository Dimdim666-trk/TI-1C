import cv2
from cvzone.HandTrackingModule import HandDetector

# 1. Inisialisasi Kamera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Kamera tidak bisa dibuka. Coba index 1/2.")

# 2. Inisialisasi Hand Detector
# staticMode: False (deteksi pada setiap frame)
# maxHands: 1 (deteksi maksimum 1 tangan)
detector = HandDetector(
    staticMode=False,
    maxHands=1,
    modelComplexity=1,
    detectionCon=0.5,
    minTrackCon=0.5
)

# 3. Loop Utama
while True:
    # Baca Frame
    ok, img = cap.read()
    if not ok:
        break

    # Temukan Tangan
    # flipType=True memberikan efek mirror pada tampilan (cocok untuk webcam)
    hands, img = detector.findHands(img, draw=True, flipType=True)

    # Proses Tangan yang Terdeteksi
    if hands:
        hand = hands[0]  # Ambil data tangan pertama
        
        # Cek jari yang terangkat (list 5 elemen: 0/1)
        # Contoh: [0, 1, 1, 0, 0] -> Jempol ke bawah, 2 jari terangkat, 2 jari ke bawah
        fingers = detector.fingersUp(hand)
        
        # Hitung jumlah jari yang terangkat
        count = sum(fingers)
        
        # Tampilkan jumlah jari dan status fingersUp pada frame
        cv2.putText(img, f"Fingers: {count} {fingers}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Tampilkan Frame dan Keluar
    cv2.imshow("Hands + Fingers", img)
    
    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 4. Pembersihan (Cleanup)
cap.release()
cv2.destroyAllWindows()