import streamlit as st
import pandas as pd
import plotly.express as px

# Memuat Dataset
@st.cache
def load_data():
    data = pd.read_csv('dataset visdat.csv')
    data['Tanggal Datang'] = pd.to_datetime(data['Tanggal Datang'])
    data['Tanggal Pulang'] = pd.to_datetime(data['Tanggal Pulang'])
    # Menghapus baris dengan nilai 9999 di kolom Diagnosis
    data = data[data['Diagnosis'] != '9999']
    return data

df = load_data()

# Filter Sidebar
st.sidebar.header("Filter")
provinsi = st.sidebar.multiselect(
    "Pilih Provinsi:",
    options=df['Provinsi Faskes'].unique(),
    default=df['Provinsi Faskes'].unique()
)
tanggal_mulai = st.sidebar.date_input("Tanggal Mulai:", df['Tanggal Datang'].min())
tanggal_selesai = st.sidebar.date_input("Tanggal Selesai:", df['Tanggal Datang'].max())

# Terapkan Filter
data_terfilter = df[
    (df['Provinsi Faskes'].isin(provinsi)) &
    (df['Tanggal Datang'] >= pd.to_datetime(tanggal_mulai)) &
    (df['Tanggal Datang'] <= pd.to_datetime(tanggal_selesai))
]

# Tab Navigasi
tabs = st.tabs(["Ringkasan Data",  "Analisis Tren", "Insight Diagnosis", "Distribusi Provinsi"])

# Tab Ringkasan Data
with tabs[0]:
    st.header("Ringkasan Data")
    st.write("Menampilkan data yang telah difilter, termasuk tabel data dan statistik deskriptif untuk memberikan pemahaman menyeluruh.")
    st.write(data_terfilter)
    st.write(f"Total Data: {data_terfilter.shape[0]}")
    st.download_button("Unduh Data yang Difilter", data=data_terfilter.to_csv(index=False), file_name="data_terfilter.csv")

# Tab Analisis Tren
with tabs[1]:
    st.header("Analisis Tren")
    st.write("Melihat pola dan tren dalam data berdasarkan waktu, seperti jumlah kunjungan atau kejadian pada hari tertentu.")
    kunjungan_per_waktu = data_terfilter.groupby('Tanggal Datang').size().reset_index(name='Jumlah')
    fig = px.line(kunjungan_per_waktu, x='Tanggal Datang', y='Jumlah', title="Kunjungan dari Waktu ke Waktu")
    st.plotly_chart(fig)

# Tab Insight Diagnosis
with tabs[2]:
    st.header("Insight Diagnosis")
    st.write("Menampilkan distribusi diagnosis paling umum dalam dataset beserta frekuensinya.")
    jumlah_diagnosis = data_terfilter['Diagnosis'].value_counts().head(10).reset_index()
    jumlah_diagnosis.columns = ['Diagnosis', 'Jumlah']
    fig = px.bar(jumlah_diagnosis, x='Jumlah', y='Diagnosis', orientation='h', title="10 Diagnosis Teratas")
    st.plotly_chart(fig)

# Tab Distribusi Provinsi
with tabs[3]:
    st.header("Distribusi Provinsi")
    st.write("Menganalisis distribusi data berdasarkan provinsi untuk mendapatkan wawasan tentang perbedaan antar wilayah.")
    jumlah_per_provinsi = data_terfilter['Provinsi Faskes'].value_counts().reset_index()
    jumlah_per_provinsi.columns = ['Provinsi', "Jumlah"]
    fig = px.bar(jumlah_per_provinsi, x='Jumlah', y='Provinsi', orientation='h', title="Kunjungan per Provinsi")
    st.plotly_chart(fig)
