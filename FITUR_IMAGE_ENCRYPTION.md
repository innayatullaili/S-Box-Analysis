# Fitur Image Encryption - Dokumentasi

## 📋 Ringkasan

Fitur Image Encryption telah ditambahkan ke S-Box Analysis Dashboard dengan dukungan penuh untuk:
- **Enkripsi Gambar**: Enkripsi gambar menggunakan algoritma AES
- **Metrik NPCR**: Analisis Number of Pixels Change Rate
- **Metrik UACI**: Analisis Unified Average Change in Intensity
- **Histogram Analysis**: Visualisasi distribusi intensitas piksel
- **Dekripsi Gambar**: Kemampuan untuk mendekripsi kembali gambar terenkripsi

---

## 🔐 Fitur Utama

### 1. Enkripsi Gambar
- **Algoritma**: AES S-box substitution dengan XOR
- **Ukuran Kunci**: 128-bit (16 karakter)
- **Format Gambar**: Mendukung semua format gambar web (PNG, JPG, GIF, BMP, WebP)
- **Saluran**: Enkripsi saluran RGB (Alpha channel tetap terjaga)

### 2. Analisis NPCR (Number of Pixels Change Rate)
**Deskripsi:**
NPCR mengukur persentase piksel yang berubah antara gambar asli dan gambar terenkripsi. Metrik ini penting untuk memastikan bahwa enkripsi mengubah semua atau hampir semua piksel.

**Rumus:**
```
NPCR = (D / (W × H)) × 100%
```

Dimana:
- D = jumlah piksel yang berbeda (di mana minimal satu channel RGB berbeda)
- W = lebar gambar (pixels)
- H = tinggi gambar (pixels)

**Nilai Ideal:**
- > 99% menunjukkan enkripsi yang sangat baik
- < 95% mungkin menunjukkan algoritma yang lemah

**Interpretasi:**
- Nilai tinggi (> 99%): Algoritma enkripsi bekerja dengan baik, hampir semua piksel berubah
- Nilai rendah (< 50%): Enkripsi mungkin tidak efektif

### 3. Analisis UACI (Unified Average Change in Intensity)
**Deskripsi:**
UACI mengukur rata-rata perubahan intensitas (brightness) piksel antara gambar asli dan terenkripsi. Ini membantu menentukan apakah perubahan piksel terdistribusi secara acak.

**Rumus:**
```
UACI = (1 / (W × H × 255)) × Σ|Asli[i,j] - Enkripsi[i,j]|
```

Dimana:
- Σ adalah penjumlahan untuk semua piksel (i,j) di semua saluran RGB
- 255 adalah nilai maksimum intensitas (8-bit)

**Nilai Ideal:**
- ≈ 33% (1/3) menunjukkan distribusi yang acak dan ideal
- Jika semua piksel berubah pada rata-rata 85 dari 255, maka UACI ≈ 33%

**Interpretasi:**
- Nilai 30-35%: Enkripsi sangat baik, distribusi acak
- Nilai < 20%: Mungkin ada pola atau struktur dalam enkripsi
- Nilai > 40%: Enkripsi ekstrem tetapi mungkin kurang efisien

### 4. Histogram Analysis
**Deskripsi:**
Histogram menunjukkan distribusi frekuensi nilai intensitas (0-255) untuk masing-masing saluran warna (Red, Green, Blue).

**Histogram Asli:**
- Menunjukkan karakteristik alami gambar asli
- Dapat memiliki pola spesifik sesuai konten gambar
- Mengungkapkan informasi tentang komposisi warna gambar

**Histogram Terenkripsi:**
- Harus menunjukkan distribusi yang hampir uniform/merata
- Puncak dan lembah yang ada di histogram asli harus hilang
- Nilai dari 0-255 harus memiliki frekuensi yang kurang lebih sama

**Analisis Keamanan:**
- **Histogram Datar (Uniform)**: Indikasi enkripsi yang baik
- **Histogram dengan Puncak**: Mungkin ada informasi bocor
- **Nilai entropy yang tinggi**: Menunjukkan randomness yang baik

---

## 🖥️ Cara Menggunakan

### Langkah 1: Upload Gambar
1. Klik tombol **"📤 Upload Image"**
2. Pilih file gambar dari komputer Anda
3. Gambar akan ditampilkan di panel "Original Image"

### Langkah 2: Masukkan Kunci Enkripsi
1. Di bagian "Encryption Settings", masukkan kunci enkripsi
2. Kunci harus berupa 16 karakter (akan di-pad dengan spasi jika kurang)
3. Gunakan kunci yang sama untuk mendekripsi

### Langkah 3: Enkripsi Gambar
1. Klik tombol **"🔐 Encrypt Image"**
2. Sistem akan:
   - Mengenkripsi gambar
   - Menghitung metrik NPCR dan UACI
   - Generate histogram untuk kedua gambar
   - Menampilkan hasil analisis

### Langkah 4: Analisis Hasil
- Lihat nilai NPCR dan UACI di metric cards
- Periksa histogram untuk melihat perubahan distribusi
- Baca deskripsi untuk interpretasi metrik

### Langkah 5: Download Hasil
- **Download Encrypted Image**: Simpan gambar terenkripsi
- **Download Analysis Report**: Simpan laporan analisis dalam format teks

### Dekripsi Gambar (Opsional)
1. Klik tombol **"🔓 Decrypt Image"** (aktif setelah enkripsi)
2. Gunakan kunci yang sama dengan enkripsi
3. Gambar akan dikembalikan ke bentuk aslinya

---

## 📊 Contoh Hasil Analisis

### Gambar Berkualitas Baik (Enkripsi Efektif)
```
NPCR: 99.8%      → Hampir semua piksel berubah
UACI: 33.2%      → Distribusi perubahan acak
Histogram: Rata   → Tidak ada pola terlihat
```

### Gambar Berkualitas Buruk (Enkripsi Lemah)
```
NPCR: 70%        → Banyak piksel tidak berubah
UACI: 15%        → Perubahan terpusat pada nilai tertentu
Histogram: Puncak → Ada pola yang terlihat
```

---

## 🔧 Implementasi Teknis

### File-file Terkait:
- **image-encryption.js**: Modul enkripsi dan analisis gambar
- **index.html**: UI untuk fitur image encryption
- **style.css**: Styling untuk tampilan image encryption

### Teknologi:
- **Chart.js**: Visualisasi histogram
- **Canvas API**: Manipulasi gambar
- **AES S-box**: Substitusi cryptographic
- **PRNG**: Pseudo-random number generator untuk keystream

### Algoritma Enkripsi:
1. **Key Expansion**: Kunci di-expand menjadi keystream menggunakan PRNG
2. **Substitution**: Setiap nilai piksel disubstitusi menggunakan AES S-box
3. **XOR Operation**: Hasil substitusi di-XOR dengan keystream
4. **Channel Preservation**: Alpha channel tidak dienkripsi

---

## ⚠️ Catatan Penting

1. **Kunci**: Simpan kunci enkripsi dengan aman jika ingin mendekripsi
2. **Format**: Enkripsi bekerja untuk gambar warna RGB (8-bit per channel)
3. **Ukuran**: Semakin besar gambar, semakin lama waktu enkripsi
4. **Browser**: Gunakan browser modern yang mendukung Canvas API
5. **Keamanan**: Algoritma ini untuk tujuan pembelajaran, bukan untuk produksi

---

## 📚 Referensi

- **NPCR & UACI**: Standar metrik untuk evaluasi enkripsi gambar
- **AES S-box**: Digunakan dalam standar Advanced Encryption Standard (FIPS 197)
- **Histogram Analysis**: Teknik analisis visual untuk evaluasi distribusi

---

## 🎯 Fitur Masa Depan

- [ ] Dukungan enkripsi multi-layer
- [ ] Berbagai pilihan algoritma enkripsi
- [ ] Analisis entropy
- [ ] Correlation analysis
- [ ] Batch processing multiple images
- [ ] WebWorker untuk enkripsi gambar besar tanpa blocking UI

---

**Dibuat untuk:** Mata Kuliah Kriptografi, Semester 5
**Platform:** S-Box Analysis Dashboard v2.0
