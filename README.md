# 📊 Dashboard Pemesanan Hotel

Visualisasi interaktif data pemesanan hotel berbasis **Streamlit** + **Plotly**.  
Dashboard ini dirancang untuk menyajikan **insight otomatis** dari data pemesanan hotel seperti durasi inap, total biaya, dan metode pembayaran — sebagai bagian dari **rangkaian riset integrasi smart contract dalam ekosistem pariwisata digital**.
 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16763254.svg)](https://doi.org/10.5281/zenodo.16763254)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stc-insight.streamlit.app/)
![STC Module – Insight](https://img.shields.io/badge/STC%20Module-Insight-purple)
![status: stable](https://img.shields.io/badge/status-stable-brightgreen)
[![Keep Alive](https://github.com/mrbrightsides/dashboard-EDA/actions/workflows/ping.yml/badge.svg)](https://github.com/mrbrightsides/dashboard-EDA/actions/workflows/ping.yml)


---

## 🚀 Fitur Utama

- ✅ Dropdown variabel X/Y & kolom warna
- ✅ Scatter, Bar, Line, Box, Pie, Histogram, dan Heatmap
- ✅ Insight otomatis (mean, hotel favorit, total biaya tertinggi, dll)
- ✅ Checkbox Tabel Data
- ✅ Tombol Unduh Dataset (CSV)
- ✅ Debug Mode (opsional)

---

## 📂 File Penting

- `app.py` — File utama Streamlit App
- `Dataset_Pemesanan_Hotel_1000Baris.csv` — Dataset sintetis (untuk simulasi)
- `requirements.txt` — Daftar dependensi untuk deploy

---

## ▶️ Jalankan Secara Lokal

```bash
# Install dependensi
pip install -r requirements.txt

# Jalankan Streamlit
streamlit run app.py
