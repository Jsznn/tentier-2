# Tutorial Streamlit

Dokumen ini berisi panduan langkah demi langkah untuk membuat, mengelola, dan men-deploy aplikasi data science sederhana menggunakan Streamlit.

## 1. Persiapan Software & Akun

### Download & Install Software
*   **Anaconda**: Unduh dari situs resmi Anaconda dan instal versi yang sesuai dengan sistem operasi Anda.
*   **Visual Studio Code**: Unduh dari situs resmi VSCode dan instal.
*   **Git**: Unduh dari situs resmi Git SCM dan instal.

### Pembuatan Akun
*   **GitHub**: Buat akun di github.com jika belum punya.
*   **Streamlit Cloud**: Buka share.streamlit.io dan pilih opsi **Sign up with GitHub**. Ini penting agar akun Streamlit Anda terhubung langsung dengan repositori kode Anda.

## 2. Konfigurasi Terminal (Khusus Windows)

Untuk pengguna Windows, Anda perlu mengatur kebijakan eksekusi agar dapat menjalankan skrip Anaconda di terminal.

1.  Cari "PowerShell" di menu Start.
2.  Klik kanan pada "Windows PowerShell" dan pilih **Run as Administrator**.
3.  Jalankan perintah berikut di dalam PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```

Ketik `Y` atau `A` jika diminta konfirmasi.

## 3. Setup Environment Project

Langkah ini akan menyiapkan folder kerja dan lingkungan Python yang terisolasi.

1.  Buat folder baru untuk proyek Anda, lalu buka folder tersebut menggunakan VSCode.
2.  Buka terminal di VSCode (Terminal > New Terminal).
3.  Buat environment baru dengan Python 3.9 bernama `myenv`:

```bash
conda create -n myenv python=3.9
```

4.  Aktifkan environment yang baru dibuat:

```bash
conda activate myenv
```

5.  Install library yang dibutuhkan:

```bash
pip install streamlit pandas numpy matplotlib seaborn
```

## 4. Cara Upload ke GitHub

Agar aplikasi dapat di-deploy, kode harus disimpan di GitHub.

1.  **Membuat requirements.txt**: File ini memberi tahu server library apa saja yang perlu diinstal. Jalankan perintah ini di terminal:

```bash
pip list --format=freeze > requirements.txt
```

2.  **Inisialisasi dan Upload ke Git**:
    Jalankan perintah berikut satu per satu di terminal VSCode:

```bash
git init
git add .
git commit -m "Commit pertama aplikasi streamlit"
git branch -M main
```

### Troubleshooting Git
Jika Anda mengalami error saat menjalankan perintah git (seperti "Please tell me who you are"), jalankan perintah berikut untuk mengonfigurasi username dan email Anda:

```bash
git config --global user.email "email_anda@example.com"
git config --global user.name "Nama Anda"
```

3.  Buat repositori baru di GitHub (tanpa file README, .gitignore, atau license agar kosong).
4.  Salin URL repositori baru Anda (contoh: `https://github.com/username/nama-repo.git`), lalu jalankan:

```bash
git remote add origin URL_REPO_ANDA_DISINI
git push -u origin main
```

*(Ganti `URL_REPO_ANDA_DISINI` dengan link repositori GitHub Anda)*

## 5. Deploy ke Streamlit Cloud

Langkah terakhir adalah mempublikasikan aplikasi agar bisa diakses orang lain.

1.  Buka share.streamlit.io.
2.  Klik tombol **New app**.
3.  Pada formulir "Deploy an app":
    *   **Repository**: Pilih repositori yang baru saja Anda upload.
    *   **Branch**: Pilih `main`.
    *   **Main file path**: Pilih atau ketik `app.py` (file streamlit).
4.  Klik tombol **Deploy**.

Tunggu proses instalasi selesai. Setelah itu, aplikasi Anda akan live dan dapat diakses melalui URL yang diberikan.
