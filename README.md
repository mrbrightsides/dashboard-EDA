# 📊 Exploratory Data Analysis Dashboard

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

## 🪄 Alur Kerja

```mermaid
flowchart LR
  U["👤 User"]
  UI["🖥️ STC Insight (Streamlit)"]
  U --> UI
  click UI "https://stc-insight.streamlit.app" "Open STC Insight" _blank
```

## High-level Architecture

```mermaid
graph TD
  U["👤 User"] --> UI["🖥️ STC Insight (Streamlit)"]

  subgraph Inputs
    CSV["📄 CSV / XLSX"]
    NDJ["🧩 NDJSON (opsional)"]
    DEMO["🗂️ Demo Dataset (opsional)"]
  end

  CSV --> UI
  NDJ --> UI
  DEMO --> UI

  UI --> CFG["⚙️ Konfigurasi\n(delimiter, decimal, sampling)"]
  UI --> PARSE["🧪 Parsing & Validasi\n(pandas)"]
  PARSE --> DF["🧱 DataFrame"]

  subgraph EDA & Viz
    CHART["📊 Charts (Altair/Plotly)"]
    HEAT["🔥 Heatmap Otomatis"]
    PREV["🔎 Preview 5 baris"]
  end

  DF --> CHART
  DF --> HEAT
  DF --> PREV

  subgraph Output
    EXP["⬇️ Export PNG/CSV"]
    TPL["⬇️ Download Template CSV"]
  end

  UI --> EXP
  UI --> TPL

  DF --> CACHE["🗃️ Cache Ringan\n(Streamlit cache)"]
```

---

## Sequence: Upload → Render Chart

```mermaid
sequenceDiagram
  participant U as User
  participant UI as STC Insight (Streamlit)
  participant P as Parser (pandas)
  participant V as Viz (Altair/Plotly)

  U->>UI: Pilih delimiter & decimal
  U->>UI: Upload file (CSV/XLSX) atau pilih Demo Dataset
  UI->>P: Baca file + infer dtype
  P-->>UI: DataFrame + info kolom
  UI->>UI: Validasi kolom x/y/color sesuai pilihan
  UI->>V: Render chart (scatter/bar/line, dsb.)
  V-->>UI: Figure siap tampil
  UI-->>U: Tampilkan chart, preview 5 baris
  U->>UI: Export PNG/CSV (opsional)
```

---

## Data Pipeline Ringkas

```mermaid
flowchart LR
  IN["Input File"] --> CLEAN["Clean & Sanitize\n(trim, NA, tanggal)"]
  CLEAN --> INFER["Type Inference\n(numeric, categorical, date)"]
  INFER --> FE["Feature Ops\n(binning durasi, mapping kota)"]
  FE --> MAP["Chart Mapping\n(x, y, color, size)"]
  MAP --> RENDER["Render Chart"]
  RENDER --> OUT["Export PNG/CSV"]
```

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
```

---

## 📜 Lisensi

MIT License © ELPEEF Dev Team
