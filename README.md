# Webcam Controller & Capture (OpenCV)

Program Python sederhana menggunakan library **OpenCV** untuk mengakses dan menampilkan *live preview* webcam, mengatur konfigurasi kamera (resolusi, exposure, gain), serta mengambil foto (single capture dan burst capture).

Proyek ini dibuat untuk keperluan pengujian / pemenuhan tugas teknis.

---

## Fitur

1. **Live Preview**: Menampilkan video stream secara real-time dari webcam menggunakan `cv2.imshow`.
2. **On-Screen Display (OSD)**: Informasi FPS, status *LIVE* / *BURST*, dan notifikasi saat foto berhasil disimpan.
3. **Konfigurasi Kamera**: Variabel di awal kode untuk mengatur resolusi frame (`width`, `height`), target FPS, serta opsi manual untuk `exposure` dan `gain`.
4. **Single Capture**: Menekan tombol `c` akan menyimpan 1 frame foto dengan penamaan timestamp.
5. **Burst Capture**: Menahan tombol `SPASI` akan mengambil dan menyimpan foto secara beruntun dan berhenti otomatis ketika tombol dilepas.
6. **Error Handling**: Penanganan saat webcam tidak terdeteksi atau koneksi terputus.

---

## Struktur Folder

```text
.
├── captures/           # Folder tempat foto disimpan (dibuat otomatis)
├── main.py             # Script utama program
├── requirements.txt    # Daftar dependensi library
└── README.md           # Dokumentasi proyek
```

---

## Prasyarat & Instalasi

Pastikan komputer sudah terpasang **Python 3.8+**.

1. **Clone atau download repositori ini**:
   ```bash
   git clone [(https://github.com/Rezahans/IOT-Embedded-Systems.git)
   cd "IOT Embedded Systems"
   ```

2. **(Opsional) Buat virtual environment**:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Instal dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Cara Menjalankan

Jalankan perintah berikut di terminal:

```bash
python main.py
```

Foto yang diambil akan otomatis tersimpan di dalam folder `captures/` dengan format:
- Single: `captures/single_YYYYMMDD_HHMMSS_mmm.jpg`
- Burst: `captures/burst_01_YYYYMMDD_HHMMSS_mmm.jpg`

---

## Kontrol Keyboard (Shortcut)

| Tombol | Aksi | Keterangan |
| :---: | :--- | :--- |
| **`c`** / **`C`** | Single Capture | Mengambil 1 jepretan foto |
| **`SPASI` (Tahan)** | Burst Capture | Mengambil foto beruntun selama tombol ditahan |
| **`q`** / **`Q`** / **`ESC`** | Keluar | Menghentikan program dan menutup jendela |

---

## Konfigurasi Parameter

Parameter kamera dapat diubah langsung di baris atas file `main.py`:

```python
CAMERA_INDEX = 0      # 0 untuk webcam bawaan, 1 jika menggunakan USB webcam
FRAME_WIDTH = 1280    # Resolusi lebar
FRAME_HEIGHT = 720    # Resolusi tinggi
FPS = 30              # Target FPS
EXPOSURE = None       # Atur angka exposure manual (misal: -5) atau None untuk auto
GAIN = None           # Atur nilai gain/ISO jika sensor mendukung, atau None untuk auto
```

> **Catatan Hardware**: Tidak semua driver/hardware webcam mengizinkan pengaturan `exposure` dan `gain` manual melalui OpenCV. Pada banyak perangkat, parameter ini dikunci secara otomatis oleh firmware kamera.

---

## Pendekatan Burst Capture

OpenCV `cv2.waitKey()` tidak memiliki pendeteksi event *key-up* (saat tombol dilepas). Pendekatan yang digunakan:
- Saat tombol keyboard ditahan, sistem operasi secara otomatis mengirimkan sinyal penekanan berulang (*auto-repeat*).
- Program mencatat waktu terakhir tombol `SPASI` diterima.
- Jika jeda waktu belum melewati batas `BURST_TIMEOUT` (0.35 detik), status burst dianggap aktif dan frame disimpan berkala sesuai `BURST_INTERVAL` (0.15 detik).
- Saat tombol dilepas, sinyal berhenti, batas waktu terlampaui, dan burst capture otomatis diselesaikan.

---

## Spesifikasi Lingkungan Pengujian

*(Bagian ini dapat diisi sesuai spesifikasi komputer penguji)*

### 1. Sistem Operasi
| Komponen | Spesifikasi |
| :--- | :--- |
| **Sistem Operasi** | [Contoh: Windows 11 Home 64-bit] |
| **Versi / Build** | [Contoh: Version 23H2 / Build 22631] |

### 2. Perangkat Keras (Hardware)
| Komponen | Spesifikasi |
| :--- | :--- |
| **Perangkat / Laptop** | [Contoh: ASUS TUF Gaming F15] |
| **Processor** | [Contoh: Intel Core i7-12700H] |
| **RAM** | [Contoh: 16 GB DDR4] |
| **Tipe Webcam** | [Contoh: Integrated Webcam 720p HD] |

### 3. Software & Library
| Software | Versi |
| :--- | :--- |
| **Python** | [Contoh: 3.12.3] |
| **OpenCV** | [Contoh: 4.13.0] |
