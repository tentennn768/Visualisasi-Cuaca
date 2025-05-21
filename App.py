import streamlit as st
import pandas as pd
import plotly.express as px

# Judul
st.title("📊 Visualisasi Data Cuaca Harian")

# Dataset dummy
data = {
    "Tanggal": pd.date_range(start="2025-01-01", periods=30),
    "Suhu (°C)": [28 + (i % 5) + (i * 0.1) for i in range(30)],
    "Kelembaban (%)": [80 - (i % 3) * 2 for i in range(30)],
    "Curah Hujan (mm)": [5 if i % 4 == 0 else 0 for i in range(30)],
}
df = pd.DataFrame(data)

# Filter tanggal
st.sidebar.header("🔍 Filter")
tanggal_mulai = st.sidebar.date_input("Tanggal mulai", df["Tanggal"].min())
tanggal_selesai = st.sidebar.date_input("Tanggal selesai", df["Tanggal"].max())

# Validasi range
if tanggal_mulai > tanggal_selesai:
    st.sidebar.error("❗ Tanggal mulai harus lebih awal dari tanggal selesai.")
else:
    df_filtered = df[(df["Tanggal"] >= pd.to_datetime(tanggal_mulai)) & (df["Tanggal"] <= pd.to_datetime(tanggal_selesai))]

    # Pilihan parameter
    parameter = st.sidebar.selectbox("Pilih parameter cuaca", ["Suhu (°C)", "Kelembaban (%)", "Curah Hujan (mm)"])

    # Jenis grafik
    chart_type = st.sidebar.radio("Jenis grafik", ["Line Chart", "Bar Chart"])

    # Plot grafik
    st.subheader(f"Grafik: {parameter}")
    if chart_type == "Line Chart":
        fig = px.line(df_filtered, x="Tanggal", y=parameter, title=f"{parameter} Harian")
    else:
        fig = px.bar(df_filtered, x="Tanggal", y=parameter, title=f"{parameter} Harian")

    st.plotly_chart(fig, use_container_width=True)

    # Tampilkan data tabel
    with st.expander("📋 Tampilkan Tabel Data"):
        st.dataframe(df_filtered)
