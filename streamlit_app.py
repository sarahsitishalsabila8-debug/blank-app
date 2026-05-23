import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# KONFIGURASI HALAMAN & SESSION STATE
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Kalkulator IKU",
    page_icon="💨",
    layout="wide"
)

# Inisialisasi state untuk menyimpan data input ( agar tidak hilang saat interaksi )
if 'list_no2' not in st.session_state:
    st.session_state['list_no2'] = []
if 'list_so2' not in st.session_state:
    st.session_state['list_so2'] = []

# -----------------------------------------------------------------------------
# FUNGSI UTAMA (LOGIC)
# -----------------------------------------------------------------------------
def hitung_iku(no2_data, so2_data):
    if not no2_data or not so2_data:
        return 0, 0, 0, 0

    # Baku Mutu EU
    bm_no2 = 40.00
    bm_so2 = 20.00

    # 1. Rerata
    rerata_no2 = sum(no2_data) / len(no2_data)
    rerata_so2 = sum(so2_data) / len(so2_data)

    # 2. Rumus 1 & 2: Indeks
    idx_no2 = rerata_no2 / bm_no2
    idx_so2 = rerata_so2 / bm_so2

    # 3. Rumus 3: IEU (Indeks Udara Eropa)
    ieu = (idx_no2 + idx_so2) / 2

    # 4. Rumus 4: IKU
    # Rumus: 100 - ((50/0,9) x (IEU-0,1))
    iku = 100 - ((50 / 0.9) * (ieu - 0.1))
    
    return idx_no2, idx_so2, ieu, iku

# -----------------------------------------------------------------------------
# NAVIGASI SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.title("Navigasi Menu")
menu_options = ["Beranda", "Pengenalan & Baku Mutu", "Perhitungan IKU"]
choice = st.sidebar.radio("Pilih Halaman:", menu_options)

# Image untuk sidebar (Opsional estetika)
st.sidebar.markdown("---")
st.sidebar.info("Proyek Analisis Kualitas Udara")

# -----------------------------------------------------------------------------
# TAMPILAN HALAMAN
# -----------------------------------------------------------------------------

# -----------------------
# HALAMAN 1: BERANDA
# -----------------------
if choice == "Beranda":
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Perhitungan Indeks Kualitas Udara (IKU)</h1>", unsafe_allow_html=True)
    
    # Gambar Unsur Kimia udara (Placeholder)
    st.image("https://images.unsplash.com/photo-1574267432553-4b4628081c31?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", caption="Aspek Kimia Udara Ambien", use_container_width=True)
    
    st.markdown("### Disusun Oleh:")
    st.markdown("""
    <ul>
        <li><b>1. Ariq</b></li>
        <li><b>2. Endhyeto</b></li>
        <li><b>3. Kahlil</b></li>
        <li><b>4. Surya</b></li>
        <li><b>5. Affan</b></li>
    </ul>
    """, unsafe_allow_html=True)

# -----------------------
# HALAMAN 2: PENGENALAN
# -----------------------
elif choice == "Pengenalan & Baku Mutu":
    # Judul dan Gambar
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Pengenalan dan Baku Mutu</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Sulfur_dioxide_3D_ball.png/640px-Sulfur_dioxide_3D_ball.png", caption="Struktur Senyawa SO2", use_container_width=True)
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Nitrogen_dioxide_3D_ball.png/640px-Nitrogen_dioxide_3D_ball.png", caption="Struktur Senyawa NO2", use_container_width=True)

    st.markdown("---")
    st.subheader("Dasar Hukum:")
    st.markdown("Berdasarkan **Lampiran II Peraturan Menteri LHK RI no.27 Tahun 2021**")

    st.write("""
    Dalam menentukan indeks kualitas udara (IKU) digunakan metode perhitungan indeks NO2 dan SO2 pada udara ambient, kemudian dilanjutkan dengan menghitung Indeks Udara Referensi EU (Uni Eropa) atau disingkat IEU. 
    Angka ini digunakan di Indonesia sebagai salah satu parameter perhitungan Indeks Kualitas Lingkungan Hidup (IKLH) berdasarkan Permen LHK Nomor 27 Tahun 2021 sekaligus menentukan kategori kualitas udara di daerah tertentu.
    """)

    # Tabel Baku Mutu dan Kategori
    c1, c2 = st.columns(2)
    
    with c1:
        st.info("Baku Mutu Referensi EU (Mikrogram/m³)")
        data_baku = {
            'Parameter': ['NO2', 'SO2'],
            'Baku Mutu (μg/m³)': [40.00, 20.00]
        }
        df_baku = pd.DataFrame(data_baku)
        st.table(df_baku)

    with c2:
        st.info("Kategori Hasil IKU")
        data_kategori = {
            'Skor IKU': ['90-100', '70-90', '50-70', '25-50', '0-25'],
            'Kategori': ['Sangat Baik', 'Baik', 'Sedang', 'Kurang', 'Sangat Kurang']
        }
        df_kat = pd.DataFrame(data_kategori)
        # Mengurutkan dari tinggi ke rendah agar sesuai logika
        df_kat = df_kat.sort_index(ascending=False)
        st.table(df_kat)

# -----------------------
# HALAMAN 3: PERHITUNGAN
# -----------------------
elif choice == "Perhitungan IKU":
    st.markdown("<h1 style='text-align: center; color: #2E86C1;'>Menghitung IKU</h1>", unsafe_allow_html=True)
    st.markdown("Silakan input data kadar NO2 dan SO2 minimal 1 data (unlimited data).")
    
    # Layout Input Data
    col_input1, col_input2 = st.columns(2)
    
    # --- Input NO2 ---
    with col_input1:
        st.subheader("Input Data NO2 (μg/m³)")
        no2_val = st.number_input("Masukkan kadar NO2", min_value=0.0, step=0.1, key="in_no2")
        if st.button("Tambah Data NO2", key="btn_no2"):
            st.session_state['list_no2'].append(no2_val)
            st.success(f"Data NO2 ditambahkan! Total data: {len(st.session_state['list_no2'])}")
        
        st.write("Data NO2 yang diinput:")
        if st.session_state['list_no2']:
            st.write(st.session_state['list_no2'])
        else:
            st.write("-")

    # --- Input SO2 ---
    with col_input2:
        st.subheader("Input Data SO2 (μg/m³)")
        so2_val = st.number_input("Masukkan kadar SO2", min_value=0.0, step=0.1, key="in_so2")
        if st.button("Tambah Data SO2", key="btn_so2"):
