# 📊 Hotel Booking Dashboard

An interactive data visualization dashboard built with **Streamlit** + **Plotly**.  
This dashboard is designed to provide **automatic insights** from hotel booking data, such as length of stay, total cost, and payment methods — as part of a **research initiative on smart contract integration within digital tourism ecosystems**.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dashboard-eda.streamlit.app)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.16763254.svg)](https://doi.org/10.5281/zenodo.16763254)

---

## 🚀 Key Features

- ✅ Variable selection for X/Y axes & color grouping
- ✅ Multiple chart types: Scatter, Bar, Line, Box, Pie, Histogram, and Heatmap
- ✅ Automated insights (average, most popular hotel, highest total cost, etc.)
- ✅ Optional data table checkbox
- ✅ Download dataset as CSV
- ✅ Debug mode (optional)

---

## 📂 Key Files

- `app.py` — Main Streamlit application file
- `Dataset_Pemesanan_Hotel_1000Baris.csv` — Synthetic dataset (for simulation)
- `requirements.txt` — List of dependencies for deployment

---

## ▶️ Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
