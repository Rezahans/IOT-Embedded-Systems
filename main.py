"""
Webcam Controller & Live Preview menggunakan OpenCV
Tugas: Program pengontrol webcam, capture foto, dan burst capture.
"""

import os
import sys
import time
from datetime import datetime
import cv2

# ==============================================================================
# KONFIGURASI PARAMETER KAMERA & APLIKASI
# ==============================================================================
# Indeks webcam (0: webcam bawaan, 1: webcam USB eksternal)
CAMERA_INDEX = 0

# Pengaturan resolusi yang diinginkan
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 30

# Pengaturan Exposure & Gain (Opsional)
# Catatan: Tidak semua hardware/driver webcam mendukung konfigurasi manual via OpenCV.
# - Windows (DirectShow): nilai exposure biasanya dalam skala logaritmik (misal: -4 s/d -7).
# - Linux (V4L2): nilai exposure biasanya berupa integer dalam skala tertentu.
# - Beri nilai None jika ingin menggunakan pengaturan otomatis bawaan kamera.
EXPOSURE = None  # Contoh: -5 atau None
GAIN = None      # Contoh: 0, 50, atau None

# Direktori penyimpanan hasil foto
SAVE_DIR = "captures"

# Konfigurasi Burst Capture
BURST_INTERVAL = 0.15  # Jeda simpan antar frame saat burst (detik)
BURST_TIMEOUT = 0.35   # Batas waktu deteksi pelepasan tombol spasi (detik)


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================
def save_frame(frame, prefix: str = "img") -> str:
    """Menyimpan frame ke direktori captures dengan nama file berbasis timestamp."""
    os.makedirs(SAVE_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"{prefix}_{timestamp}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)
    cv2.imwrite(filepath, frame)
    return filename


def draw_hud(frame, fps: float, is_burst: bool, info_msg: str):
    """Menampilkan informasi status ringkas di atas frame video."""
    h, _ = frame.shape[:2]

    # Status koneksi & FPS
    status = "BURST CAPTURING..." if is_burst else "LIVE"
    status_color = (0, 0, 255) if is_burst else (0, 255, 0)
    cv2.putText(frame, f"FPS: {fps:4.1f} | Status: {status}", (15, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, status_color, 2, cv2.LINE_AA)

    # Notifikasi penyimpanan foto
    if info_msg:
        cv2.putText(frame, info_msg, (15, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2, cv2.LINE_AA)

    # Panduan shortcut di bagian bawah
    help_text = "[C] Capture  |  [Tahan SPASI] Burst  |  [Q / ESC] Keluar"
    cv2.putText(frame, help_text, (15, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220, 220, 220), 1, cv2.LINE_AA)


def setup_camera():
    """Membuka koneksi webcam dan mengonfigurasi parameter awal."""
    # Gunakan CAP_DSHOW di Windows untuk inisialisasi yang lebih stabil
    if sys.platform.startswith("win"):
        cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(CAMERA_INDEX)
    else:
        cap = cv2.VideoCapture(CAMERA_INDEX)

    # Error handling jika webcam gagal dibuka
    if not cap.isOpened():
        print(f"[ERROR] Webcam pada index {CAMERA_INDEX} tidak ditemukan atau tidak bisa dibuka.")
        print("Solusi: Periksa kabel webcam, izin akses privasi kamera, atau pastikan aplikasi lain tidak sedang menggunakannya.")
        return None

    # Terapkan resolusi dan FPS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    if FPS:
        cap.set(cv2.CAP_PROP_FPS, FPS)

    # Terapkan Exposure dan Gain jika diisi
    if EXPOSURE is not None:
        cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    if GAIN is not None:
        cap.set(cv2.CAP_PROP_GAIN, GAIN)

    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"[INFO] Kamera terhubung: {actual_w}x{actual_h} @ {cap.get(cv2.CAP_PROP_FPS):.1f} FPS")
    return cap


# ==============================================================================
# MAIN LOOP
# ==============================================================================
def main():
    cap = setup_camera()
    if cap is None:
        sys.exit(1)

    window_name = "Webcam Live Preview"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    # Variabel penghitung FPS
    fps = 0.0
    frame_count = 0
    start_time = time.time()

    # Variabel notifikasi
    info_msg = ""
    info_timer = 0.0

    # Variabel logika Burst Capture
    # Catatan: OpenCV waitKey tidak mendeteksi event tombol dilepas (key release).
    # Namun saat tombol keyboard ditahan, sistem operasi akan mengirimkan event key-press
    # secara berulang (keyboard auto-repeat).
    # Kita mencatat waktu terakhir tombol spasi ditekan. Selama selisih waktu masih di bawah
    # BURST_TIMEOUT, sistem menganggap tombol sedang ditahan. Begitu tombol dilepas dan waktu
    # melebihi timeout, burst capture otomatis berhenti.
    last_burst_press = 0.0
    last_burst_save = 0.0
    is_bursting = False
    burst_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("[ERROR] Frame tidak dapat dibaca dari webcam.")
                break

            current_time = time.time()

            # Hitung FPS real-time tiap 0.5 detik
            frame_count += 1
            if (current_time - start_time) >= 0.5:
                fps = frame_count / (current_time - start_time)
                frame_count = 0
                start_time = current_time

            # Simpan frame asli (clean) sebelum ditambahkan teks status/HUD
            clean_frame = frame.copy()

            # Tangani input keyboard
            key = cv2.waitKey(1) & 0xFF

            # 1. Single Capture ('c' atau 'C')
            if key in (ord('c'), ord('C')):
                filename = save_frame(clean_frame, prefix="single")
                info_msg = f"Tersimpan: {filename}"
                info_timer = current_time
                print(f"[CAPTURE] Single: {filename}")

            # 2. Deteksi tombol Spasi untuk Burst Capture
            if key == 32:  # ASCII Spasi
                last_burst_press = current_time

            # Cek apakah spasi masih dalam kondisi ditahan
            if (current_time - last_burst_press) < BURST_TIMEOUT:
                if not is_bursting:
                    is_bursting = True
                    burst_count = 0
                    print("[BURST] Mulai burst capture...")

                # Simpan gambar sesuai interval agar tidak membanjiri disk
                if (current_time - last_burst_save) >= BURST_INTERVAL:
                    burst_count += 1
                    filename = save_frame(clean_frame, prefix=f"burst_{burst_count:02d}")
                    last_burst_save = current_time
                    info_msg = f"Burst #{burst_count}: {filename}"
                    info_timer = current_time
                    print(f"  -> {filename}")
            else:
                if is_bursting:
                    is_bursting = False
                    print(f"[BURST] Selesai. Total tersimpan: {burst_count} foto.")

            # Hapus pesan notifikasi setelah 2 detik
            if info_msg and (current_time - info_timer > 2.0):
                info_msg = ""

            # 3. Keluar ('q', 'Q', atau ESC)
            if key in (ord('q'), ord('Q'), 27):
                print("[INFO] Program dihentikan.")
                break

            # Tampilkan HUD dan render frame
            draw_hud(frame, fps, is_bursting, info_msg)
            cv2.imshow(window_name, frame)

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Resource kamera dan jendela berhasil ditutup.")


if __name__ == "__main__":
    main()
