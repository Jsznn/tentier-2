# Panduan Perintah Conda (Anaconda/Miniconda)

Dokumen ini berisi kumpulan perintah Conda yang sering digunakan untuk manajemen environment dan paket Python.

## 1. Manajemen Environment

Perintah dasar untuk mengelola lingkungan kerja (virtual environment) agar library antar proyek tidak bentrok.

```bash
# Membuat environment baru dengan versi Python tertentu
# Ganti 'nama_env' dengan nama yang diinginkan (misal: tentier-env)
conda create --name nama_env python=3.9

# Mengaktifkan environment
conda activate nama_env

# Menonaktifkan environment (kembali ke base)
conda deactivate

# Melihat daftar semua environment yang ada
conda env list
# atau
conda info --envs

# Menghapus environment (Hati-hati!)
conda env remove --name nama_env
```

## 2. Manajemen Paket (Library)

Cara install, update, dan hapus library di dalam environment yang sedang aktif.

```bash
# Install paket tertentu (misal: pandas)
conda install pandas

# Install versi spesifik
conda install pandas=1.3.5

# Install beberapa paket sekaligus
conda install numpy matplotlib scikit-learn

# Install dari channel tertentu (misal: conda-forge)
conda install -c conda-forge streamlit

# Update paket
conda update pandas

# Update SEMUA paket di environment saat ini
conda update --all

# Menghapus paket
conda remove pandas

# Melihat daftar paket yang terinstall di environment saat ini
conda list
```

## 3. Export & Import Environment (Penting untuk Kolaborasi)

Cara membagikan konfigurasi environment Anda ke teman tim atau untuk deployment.

```bash
# Export konfigurasi environment aktif ke file YAML
conda env export > environment.yml

# Export hanya paket yang eksplisit diinstall (lebih bersih, lintas OS)
conda env export --from-history > environment.yml

# Membuat environment baru dari file YAML
conda env create -f environment.yml
```

## 4. Membersihkan Cache

Jika hard disk penuh karena cache Conda yang menumpuk.

```bash
# Menghapus file tarball yang tidak terpakai
conda clean --tarballs

# Membersihkan semua cache (index, lock files, tarballs, dll)
conda clean --all
```

## 5. Tips Tambahan

### A. Cek Versi Conda
```bash
conda --version
```

### B. Update Conda Core
```bash
conda update conda
```

### C. Mencari Paket
Jika tidak yakin nama paketnya.
```bash
conda search nama_paket
```
