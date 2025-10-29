import cv2
import numpy as np
from collections import deque
from cvzone.PoseModule import PoseDetector

# --- Konfigurasi Konstanta ---

MODE = "squat"  # Tekan 'm' untuk toggle mode antara "squat" dan "pushup"
# Ambang batas SQUAT (sudut lutut dalam derajat)
SQUAT_KNEE_DOWN = 80  
SQUAT_KNEE_UP = 160   
# Ambang batas PUSH-UP (rasio shoulder-wrist / shoulder-hip)
PUSHUP_DOWN_RATIO = 0.85
PUSHUP_UP_RATIO = 1.00

# Minimal frame konsisten sebelum ganti state (Debounce)
SAMPLE_OK = 4

# --- Inisialisasi Kamera & Pose Detector ---

# Menggunakan cv2.CAP_DSHOW untuk meningkatkan stabilitas kamera di Windows
# Ganti indeks 0 dengan 1 atau 2 jika kamera default gagal dibuka
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    if not cap.isOpened():
        # Coba lagi tanpa DSHOW jika DSHOW gagal atau bukan di Windows
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Kamera tidak bisa dibuka. Cek indeks kamera atau izin.")
except Exception as e:
    raise RuntimeError(f"Gagal membuka kamera: {e}")

# Inisialisasi Pose Detector
detector = PoseDetector(
    staticMode=False, 
    modelComplexity=1,
    enableSegmentation=False, 
    detectionCon=0.5, 
    trackCon=0.5
)

# Variabel status
count = 0
state = "up"
# Buffer untuk debounce
debounce = deque(maxlen=6)

# --- Fungsi Bantuan ---

def ratio_pushup(lm):
    """
    Menghitung rasio push-up: (Jarak Shoulder-Wrist) / (Jarak Shoulder-Hip).
    Menggunakan landmark kiri: 11 (Bahu), 15 (Pergelangan Tangan), 23 (Pinggul).
    """
    # Ambil koordinat x, y (indeks 1 dan 2)
    sh = np.array(lm[11][1:3])  # Shoulder (Bahu)
    wr = np.array(lm[15][1:3])  # Wrist (Pergelangan tangan)
    hp = np.array(lm[23][1:3])  # Hip (Pinggul)
    
    dist_sh_wr = np.linalg.norm(sh - wr)
    dist_sh_hp = np.linalg.norm(sh - hp)
    
    # Menghitung rasio
    return dist_sh_wr / (dist_sh_hp + 1e-8)

# --- Main Loop ---

while True:
    ok, img = cap.read()
    if not ok: 
        print("Selesai (Akhir Stream atau Gagal Baca Frame)")
        break

    # Deteksi pose dan landmark
    img = detector.findPose(img, draw=True)
    lmList, _ = detector.findPosition(img, draw=False)
    
    flag = None  # Status sementara gerakan saat ini

    if lmList:
        if MODE == "squat":
            # --- Logika Squat (Sudut Lutut) ---
            
            # Sudut lutut kiri: Hip(23)-Knee(25)-Ankle(27)
            angL, img = detector.findAngle(lmList[23][0:2], lmList[25][0:2], lmList[27][0:2],
                                           img=img, color=(0, 0, 255), scale=10)
            # Sudut lutut kanan: Hip(24)-Knee(26)-Ankle(28)
            angR, img = detector.findAngle(lmList[24][0:2], lmList[26][0:2], lmList[28][0:2],
                                           img=img, color=(0, 255, 0), scale=10)
            
            ang = (angL + angR) / 2.0
            
            # Penentuan State
            if ang < SQUAT_KNEE_DOWN: 
                flag = "down"
            elif ang > SQUAT_KNEE_UP: 
                flag = "up"
                
            # Tampilkan sudut lutut
            cv2.putText(img, f"Knee: {ang:5.1f} deg", (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                        
        else: # MODE == "pushup"
            # --- Logika Push-up (Rasio Tubuh) ---
            
            r = ratio_pushup(lmList)
            
            # Penentuan State
            if r < PUSHUP_DOWN_RATIO: 
                flag = "down"
            elif r > PUSHUP_UP_RATIO: 
                flag = "up"
                
            # Tampilkan rasio
            cv2.putText(img, f"Ratio: {r:4.2f}", (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        # --- Mekanisme Hitungan (Debounce) ---
        
        debounce.append(flag)
        
        # Transisi UP -> DOWN
        if debounce.count("down") >= SAMPLE_OK and state == "up":
            state = "down"
            
        # Transisi DOWN -> UP (Hitungan bertambah)
        if debounce.count("up") >= SAMPLE_OK and state == "down":
            state = "up"
            count += 1

    # --- Tampilkan Informasi Umum ---
    
    # Mode dan Hitungan
    cv2.putText(img, f"Mode: {MODE.upper()} Count: {count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    # State (Up/Down)
    cv2.putText(img, f"State: {state.upper()}", (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Tampilkan frame
    cv2.imshow("Pose Counter", img)
    
    # --- Input Keyboard ---
    
    key = cv2.waitKey(1) & 0xFF
    
    # Keluar (q)
    if key == ord('q'):
        break
    
    # Toggle Mode (m)
    if key == ord('m'): 
        MODE = "pushup" if MODE == "squat" else "squat"

# --- Bersihkan ---

cap.release()
cv2.destroyAllWindows()