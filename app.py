import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Dashboard Pemesanan Hotel Interaktif")

# Load data
df = pd.read_csv("Dataset_Pemesanan_Hotel_1000Baris.csv", sep=';')
df['harga_per_malam'] = pd.to_numeric(df['harga_per_malam'], errors='coerce')
df['total_biaya'] = pd.to_numeric(df['total_biaya'], errors='coerce')
df['durasi_inap'] = pd.to_numeric(df['durasi_inap'], errors='coerce')
df['jumlah_kamar'] = pd.to_numeric(df['jumlah_kamar'], errors='coerce')

# Sidebar: pilih variabel
st.sidebar.header("🔧 Pengaturan Visualisasi")
x_axis = st.sidebar.selectbox("Sumbu X", df.select_dtypes(include='number').columns)
y_axis = st.sidebar.selectbox("Sumbu Y", df.select_dtypes(include='number').columns)
color = st.sidebar.selectbox("Warna Berdasarkan", df.select_dtypes(include='object').columns)

# Grafik scatter interaktif
fig = px.scatter(df, x=x_axis, y=y_axis, color=color, hover_data=['nama_hotel', 'metode_pembayaran'])
fig.update_layout(title=f"{x_axis} vs {y_axis}", xaxis_title=x_axis, yaxis_title=y_axis)
st.plotly_chart(fig, use_container_width=True)

# Insight narasi sederhana
st.markdown("### 📌 Insight Otomatis")
st.write(f"📈 Rata-rata {x_axis}: {df[x_axis].mean():,.0f}")
st.write(f"📉 Rata-rata {y_axis}: {df[y_axis].mean():,.0f}")

# Tabel data
if st.checkbox("📋 Tampilkan Tabel Data"):
    st.dataframe(df)