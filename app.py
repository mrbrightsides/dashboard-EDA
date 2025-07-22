import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

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
chart_type = st.sidebar.selectbox("Pilih Jenis Grafik", ["Scatter", "Bar", "Pie", "Heatmap"])
x_axis = st.sidebar.selectbox("Sumbu X", df.select_dtypes(include='number').columns)
y_axis = st.sidebar.selectbox("Sumbu Y", df.select_dtypes(include='number').columns)
color = st.sidebar.selectbox("Warna Berdasarkan (opsional)", df.select_dtypes(include='object').columns)

# Visualisasi dinamis
st.subheader("📈 Hasil Visualisasi")

if chart_type == "Scatter":
    fig = px.scatter(df, x=x_axis, y=y_axis, color=color, hover_data=['nama_hotel', 'metode_pembayaran'])
    fig.update_layout(title=f"{x_axis} vs {y_axis}", xaxis_title=x_axis, yaxis_title=y_axis)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Bar":
    grouped = df.groupby(color)[x_axis].mean().reset_index().sort_values(by=x_axis, ascending=False)
    fig = px.bar(grouped, x=color, y=x_axis, color=color)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Pie":
    pie_data = df[color].value_counts().reset_index()
    pie_data.columns = [color, 'Jumlah']
    fig = px.pie(pie_data, names=color, values='Jumlah', title=f"Distribusi berdasarkan {color}")
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Heatmap":
    st.markdown("#### 🔥 Korelasi Antar Variabel Numerik")
    corr = df.select_dtypes(include='number').corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

# Insight narasi
st.markdown("### 📌 Insight Otomatis")
st.write(f"📈 Rata-rata {x_axis}: {df[x_axis].mean():,.0f}")
st.write(f"📉 Rata-rata {y_axis}: {df[y_axis].mean():,.0f}")

# Tampilkan tabel
if st.checkbox("📋 Tampilkan Tabel Data"):
    st.dataframe(df)
