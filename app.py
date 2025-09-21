import os, io
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime

if st.query_params.get("ping") == "1":
    st.write("ok"); st.stop()

# === Logo dan Header ===
LOGO_URL = "https://i.imgur.com/7j5aq4l.png"
col1, col2 = st.columns([1, 4])
with col1:
    st.image(LOGO_URL, width=60)
with col2:
    st.markdown("## STC Insight")

st.set_page_config(
    page_title="STC Insight",
    page_icon="📊",
    layout="wide"
)

# ---------- Konfigurasi halaman ----------
st.title("📊 Exploratory Data Analysis Dashboard")

with st.expander("ℹ️ Tentang STC Insight", expanded=False):
    st.markdown("""
    ## 📘 About
    
    STC Insight adalah dasbor visual interaktif untuk menganalisis data pemesanan dan biaya dalam ekosistem <a href="https://smartourism.elpeef.com/" target="_blank">SmartTourismChain (STC)</a>.

    Dashboard ini dirancang untuk membantu pelaku industri, peneliti, dan pengembang dalam mengeksplorasi data transaksi wisata secara cepat dan intuitif, mulai dari tren durasi inap, total biaya, hingga metode pembayaran dan status transaksi.
    
    **Fitur:**
    - Interactive charts  
    - CSV & NDJSON support  
    - Configurable delimiter & decimal  
    - Auto-generated heatmaps  

    ## 🧩 STC Ecosystem
    1. [STC Analytics](https://stc-analytics.streamlit.app/)
    2. [STC GasVision](https://stc-gasvision.streamlit.app/)
    3. [STC Converter](https://stc-converter.streamlit.app/)
    4. [STC Bench](https://stc-bench.streamlit.app/)
    5. [STC Insight](https://stc-insight.streamlit.app/)
    6. [STC Plugin](https://smartourism.elpeef.com/)
    7. [STC GasX](https://stc-gasx.streamlit.app/)
    8. [STC CarbonPrint](https://stc-carbonprint.streamlit.app/)
    9. [STC ImpactViz](https://stc-impactviz.streamlit.app/)
    10. [DataHub](https://stc-data.streamlit.app/)

    ## ☂ RANTAI Communities
    1. [Learn3](https://learn3.streamlit.app/)
    2. [Nexus](https://rantai-nexus.streamlit.app/)
    3. [BlockPedia](https://blockpedia.streamlit.app/)
    4. [Data Insights & Visualization Assistant](https://rantai-diva.streamlit.app/)
    5. [Exploratory Data Analysis](https://rantai-exploda.streamlit.app/)
    6. [Business Intelligence](https://rantai-busi.streamlit.app/)
    7. [Predictive Modelling](https://rantai-model-predi.streamlit.app/)
    8. [Ethic & Bias Checker](https://rantai-ethika.streamlit.app/)
    9. [Decentralized Supply Chain](https://rantai-trace.streamlit.app/)
    10. [ESG Compliance Manager](https://rantai-sentinel.streamlit.app/)
    11. [Decentralized Storage Optimizer](https://rantai-greenstorage.streamlit.app/)
    12. [Cloud Carbon Footprint Tracker](https://rantai-greencloud.streamlit.app/)
    13. [Cloud.Climate.Chain](https://rantai-3c.streamlit.app/)
    14. [Smart Atlas For Environment](https://rantai-safe.streamlit.app/)
    15. [Real-time Social Sentiment](https://rantai-rss.streamlit.app/)

    ## 🙌 Dukungan & kontributor
    - ⭐ **Star / Fork**: [GitHub repo](https://github.com/mrbrightsides/dashboard-eda)
    - Built with 💙 by [Khudri](https://s.id/khudri)
    - Dukung pengembangan proyek ini melalui: 
      [💖 GitHub Sponsors](https://github.com/sponsors/mrbrightsides) • 
      [☕ Ko-fi](https://ko-fi.com/khudri) • 
      [💵 PayPal](https://www.paypal.com/paypalme/akhmadkhudri) • 
      [🍵 Trakteer](https://trakteer.id/akhmad_khudri)

    Versi UI: v1.0 • Streamlit • Theme Dark
    </span>
    """, unsafe_allow_html=True)

# ---------- Standar kolom dataset ----------
EXPECTED = [
    "ID_pemesanan","nama_pengguna","email","nama_hotel","kota",
    "check_in","check_out","durasi_inap","jumlah_kamar",
    "harga_per_malam","total_biaya","metode_pembayaran",
    "wallet_address","status_transaksi","timestamp_pemesanan"
]

# ---------- State awal ----------
if "eda_df" not in st.session_state:
    st.session_state["eda_df"] = None

# ---------- Helper ----------
@st.cache_data
def build_template_csv() -> bytes:
    """Template kosong (header saja)."""
    return pd.DataFrame(columns=EXPECTED).to_csv(index=False).encode("utf-8")

@st.cache_data
def load_demo_csv() -> pd.DataFrame:
    """
    Opsional: dataset contoh di folder yang sama (jika ada).
    Nama file boleh kamu sesuaikan.
    """
    demo_name = "Dataset_Pemesanan_Hotel_1000Baris.csv"
    if not os.path.exists(demo_name):
        return pd.DataFrame(columns=EXPECTED)
    # default pakai ';' (ubah sesuai dataset demo-mu)
    df = pd.read_csv(demo_name, sep=";")
    return df

def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    """Casting tipe kolom agar grafik aman."""
    date_cols = ["check_in","check_out","timestamp_pemesanan"]
    num_cols  = ["durasi_inap","jumlah_kamar","harga_per_malam","total_biaya"]
    for c in date_cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def validate_columns(df: pd.DataFrame):
    missing = [c for c in EXPECTED if c not in df.columns]
    extra   = [c for c in df.columns if c not in EXPECTED]
    return missing, extra

@st.cache_data
def read_user_file(file, sep: str, decimal: str) -> pd.DataFrame:
    if file.name.lower().endswith(".csv"):
        return pd.read_csv(file, sep=sep, decimal=decimal)
    return pd.read_excel(file)

# ---------- Header: Download template + Upload ----------
top = st.container()
with top:
    c_dl, c_sp, c_prev = st.columns([1.2, 2, 1])
    with c_dl:
        st.download_button(
            "⬇️ Download template CSV",
            data=build_template_csv(),
            file_name="template_pemesanan.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with c_prev:
        preview5 = st.checkbox("Preview 5 baris", value=True)

    c1, c2 = st.columns(2)
    with c1:
        delim = st.selectbox("Delimiter CSV", [",",";","\\t"], index=0)
    with c2:
        dec = st.selectbox("Tanda desimal", [".",","], index=0)

    up = st.file_uploader(
        "Upload dataset pemesanan (CSV/XLSX)",
        type=["csv","xlsx"],
        accept_multiple_files=False
    )

# ---------- Kontrol dataset (Demo & Clear) ----------
cc1, cc2 = st.columns([1,1])
with cc1:
    use_demo = st.toggle(
        "Gunakan data demo (jika tersedia)",
        value=False,
        help="Aktifkan untuk memuat dataset contoh bila belum meng-upload."
    )
with cc2:
    if st.button("🔄 Clear dataset (mulai kosong)"):
        st.session_state["eda_df"] = None
        st.rerun()

# ---------- Load dari upload / demo ----------
if up is not None:
    try:
        df = read_user_file(up, sep=delim if delim != "\\t" else "\t", decimal=dec)
        missing, extra = validate_columns(df)
        if missing:
            st.error(f"Format CSV tidak sesuai. Kolom hilang: {', '.join(missing)}")
            st.stop()
        if extra:
            st.warning(f"Ada kolom tambahan yang tidak dikenali: {', '.join(extra)}")
        df = cast_types(df)
        st.session_state["eda_df"] = df
        st.success(f"Dataset valid ✅  ({df.shape[0]} baris, {df.shape[1]} kolom)")
        if preview5:
            st.dataframe(df.head(), use_container_width=True)
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")

df = st.session_state["eda_df"]
if df is None and use_demo:
    demo_df = load_demo_csv()
    if not demo_df.empty:
        st.session_state["eda_df"] = cast_types(demo_df)
        df = st.session_state["eda_df"]
        st.info("Memuat data demo.")
        if preview5:
            st.dataframe(df.head(), use_container_width=True)

# ---------- Empty state ----------
if df is None or df.empty:
    st.info("Belum ada data. Silakan upload CSV/XLSX sesuai template, atau aktifkan **Gunakan data demo**.")
    st.stop()

# ---------- Sidebar pengaturan visualisasi ----------
st.sidebar.header("🔧 Pengaturan Visualisasi")
chart_type = st.sidebar.selectbox(
    "Pilih Jenis Grafik",
    ["Scatter","Bar","Line","Box","Histogram","Heatmap","Pie"]
)

num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(include=["object","category"]).columns.tolist()
all_cols = df.columns.tolist()

# default pilihan sumbu
default_x = num_cols[0] if num_cols else all_cols[0]
default_y = num_cols[1] if len(num_cols) > 1 else (num_cols[0] if num_cols else None)

x_axis = st.sidebar.selectbox("Sumbu X", num_cols if chart_type != "Pie" else all_cols, index=0 if default_x in (num_cols if chart_type != "Pie" else all_cols) else 0)
y_axis = None
if chart_type in ["Scatter","Bar","Line","Box"]:
    y_axis = st.sidebar.selectbox("Sumbu Y", num_cols, index=(1 if default_y and default_y in num_cols else 0))

color_opt = st.sidebar.selectbox("Warna Berdasarkan (opsional)", [None] + all_cols, index=0)

# ---------- Plot ----------
st.subheader("🔥 Visualisasi Data")

def add_color(kwargs):
    if color_opt:
        kwargs["color"] = color_opt
    return kwargs

if chart_type == "Heatmap":
    if len(num_cols) < 2:
        st.warning("Butuh minimal 2 kolom numerik untuk Heatmap.")
    else:
        corr = df[num_cols].corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Histogram":
    if not num_cols:
        st.warning("Tidak ada kolom numerik.")
    else:
        xh = st.sidebar.selectbox("Kolom (Histogram)", num_cols)
        fig = px.histogram(df, x=xh, **add_color({}))
        st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Pie":
    if not cat_cols or not num_cols:
        st.warning("Butuh kolom kategori dan numerik untuk Pie chart.")
    else:
        names = st.sidebar.selectbox("Nama (kategori)", cat_cols)
        values = st.sidebar.selectbox("Nilai (numerik)", num_cols)
        fig = px.pie(df, names=names, values=values)
        st.plotly_chart(fig, use_container_width=True)

else:
    # Scatter / Bar / Line / Box
    if y_axis is None:
        st.warning("Pilih sumbu Y terlebih dahulu.")
    else:
        common_kwargs = add_color({"hover_data": [c for c in ["ID_pemesanan","nama_hotel","kota","metode_pembayaran","status_transaksi"] if c in df.columns]})
        if chart_type == "Scatter":
            fig = px.scatter(df, x=x_axis, y=y_axis, **common_kwargs)
        elif chart_type == "Bar":
            fig = px.bar(df, x=x_axis, y=y_axis, **common_kwargs)
        elif chart_type == "Line":
            fig = px.line(df, x=x_axis, y=y_axis, **common_kwargs)
        elif chart_type == "Box":
            fig = px.box(df, x=x_axis, y=y_axis, **common_kwargs)
        st.plotly_chart(fig, use_container_width=True)

# ---------- Ringkasan kecil ----------
with st.expander("ℹ️ Ringkasan Cepat"):
    st.write(f"Jumlah baris: **{len(df):,}**")
    if set(["durasi_inap","total_biaya"]).issubset(df.columns):
        corr_val = df[["durasi_inap","total_biaya"]].corr().iloc[0,1]
        st.write(f"Korelasi *durasi_inap ↔ total_biaya*: **{corr_val:.3f}**")
