import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Dashboard Pemesanan Hotel Interaktif")

# Load data
df = pd.read_csv("Dataset_Pemesanan_Hotel_1000Baris.csv", sep=';')
df['harga_per_malam'] = pd.to_numeric(df['harga_per_malam'], errors='coerce')
df['total_biaya'] = pd.to_numeric(df['total_biaya'], errors='coerce')
df['durasi_inap'] = pd.to_numeric(df['durasi_inap'], errors='coerce')
df['jumlah_kamar'] = pd.to_numeric(df['jumlah_kamar'], errors='coerce')

# Sidebar
st.sidebar.header("🔧 Pengaturan Visualisasi")
chart_type = st.sidebar.selectbox(
    "Pilih Jenis Grafik", 
    ["Scatter", "Bar", "Line", "Box", "Heatmap", "Pie", "Histogram"]
)

x_axis = st.sidebar.selectbox("Sumbu X", df.select_dtypes(include='number').columns)
y_axis = st.sidebar.selectbox("Sumbu Y", df.select_dtypes(include='number').columns)
color = st.sidebar.selectbox("Warna Berdasarkan (opsional)", [None] + list(df.select_dtypes(include='object').columns))

# Chart rendering
st.markdown("## 🔥 Visualisasi Data")

if chart_type == "Scatter":
    fig = px.scatter(df, x=x_axis, y=y_axis, color=color, hover_data=['nama_hotel', 'metode_pembayaran'])
    fig.update_layout(title=f"{x_axis} vs {y_axis}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Bar":
    fig = px.bar(df, x=x_axis, y=y_axis, color=color)
    fig.update_layout(title=f"Bar Chart: {x_axis} vs {y_axis}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Line":
    fig = px.line(df.sort_values(by=x_axis), x=x_axis, y=y_axis, color=color)
    fig.update_layout(title=f"Line Chart: {x_axis} vs {y_axis}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Box":
    fig = px.box(df, x=color if color else x_axis, y=y_axis)
    fig.update_layout(title=f"Box Plot: {y_axis} berdasarkan {color if color else x_axis}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Heatmap":
    st.markdown("### 🔥 Korelasi Antar Variabel Numerik")
    corr = df.select_dtypes(include='number').corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Pie":
    pie_col = st.sidebar.selectbox("Kolom untuk Pie Chart", df.select_dtypes(include='object').columns)
    pie_data = df[pie_col].value_counts().reset_index()
    pie_data.columns = [pie_col, 'count']
    fig = px.pie(pie_data, names=pie_col, values='count', title=f"Distribusi {pie_col}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Histogram":
    hist_col = st.sidebar.selectbox("Kolom untuk Histogram", df.select_dtypes(include='number').columns)
    fig = px.histogram(df, x=hist_col, nbins=30, title=f"Distribusi {hist_col}")
    st.plotly_chart(fig, use_container_width=True)

# Buat subset data untuk insight otomatis (dinamis)
subset_df = df.copy()

if chart_type == "Pie":
    subset_df = df[df[pie_col].notnull()]
elif chart_type == "Histogram":
    subset_df = df[df[hist_col].notnull()]
else:
    columns = [x_axis, y_axis]
    if color:
        columns.append(color)
    subset_df = df.dropna(subset=columns)


if 'nama_hotel' in subset_df.columns:
    st.write("🏨 Hotel Paling Sering Dipesan:", subset_df['nama_hotel'].value_counts().idxmax())
if 'total_biaya' in subset_df.columns:
    st.write("💰 Total Biaya Tertinggi:", subset_df['total_biaya'].max())
if 'metode_pembayaran' in subset_df.columns:
    st.write("🧾 Metode Pembayaran Terbanyak:", subset_df['metode_pembayaran'].value_counts().idxmax())

# Show data table
if st.checkbox("📋 Tampilkan Tabel Data"):
    st.dataframe(df)

# Download CSV
st.markdown("### 📥 Unduh Dataset")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Unduh Data CSV",
    data=csv,
    file_name='data_pemesanan_hotel.csv',
    mime='text/csv',
	)
	
try:
    mean_x = float(subset_df[x_axis].mean())
    mean_y = float(subset_df[y_axis].mean())
    st.write(f"📈 Rata-rata {x_axis}: {mean_x:,.0f}")
    st.write(f"📉 Rata-rata {y_axis}: {mean_y:,.0f}")
except Exception as e:
    st.error(f"❌ Gagal hitung rata-rata: {e}")

if st.sidebar.checkbox("🛠️ Aktifkan Debug Mode"):
    st.write("Kolom di subset_df:", subset_df.columns.tolist())
    st.write("Tipe subset_df[x_axis]:", type(subset_df[x_axis]))
    st.write("Contoh isi:", subset_df[x_axis].head())