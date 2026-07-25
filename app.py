import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ==== Load model & label encoder ====
model = joblib.load('model/model_rf.joblib')
label_encoder = joblib.load('model/label_encoder.joblib')

st.set_page_config(page_title="Prediksi Status Siswa - Jaya Jaya Institut", layout="centered")

# ==== Styling ====
st.markdown("""
<style>
    .main {
        background-color: #f7f8fa;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 900px;
    }
    h1 {
        font-weight: 700;
        color: #1a2b4c;
        border-bottom: 3px solid #2e5aac;
        padding-bottom: 0.5rem;
    }
    h3 {
        color: #2e5aac;
        margin-top: 1.5rem;
    }
    .stButton>button {
        background-color: #2e5aac;
        color: white;
        border-radius: 6px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1a3d7c;
        color: white;
    }
    .result-card {
        padding: 1.5rem 1.8rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 6px solid;
    }
    .result-dropout { background-color: #fdecea; border-color: #c0392b; }
    .result-enrolled { background-color: #eaf2fb; border-color: #2e5aac; }
    .result-graduate { background-color: #eafaf1; border-color: #27ae60; }
    .result-title { font-size: 0.85rem; color: #666; letter-spacing: 0.05em; }
    .result-status { font-size: 1.7rem; font-weight: 700; margin: 0.2rem 0; }
    .result-desc { font-size: 0.95rem; color: #333; }
</style>
""", unsafe_allow_html=True)

# ==== Header ====
st.title("Sistem Prediksi Status Siswa")
st.markdown("Alat bantu identifikasi risiko dropout siswa berdasarkan data akademik dan sosial-ekonomi.")
st.caption("Isi data siswa pada form di bawah, lalu klik tombol prediksi untuk melihat hasil analisis.")

st.divider()

# ============================================================
# ==== MAPPING LABEL -> KODE (mengikuti dokumentasi resmi dataset UCI) ====
# ============================================================

marital_map = {
    "Belum Menikah": 1, "Menikah": 2, "Duda/Janda": 3,
    "Bercerai": 4, "Persatuan Faktual (Facto Union)": 5, "Berpisah Secara Hukum": 6
}

gender_map = {"Laki-laki": 1, "Perempuan": 0}
yes_no_map = {"Ya": 1, "Tidak": 0}
attendance_map = {"Siang (Daytime)": 1, "Malam (Evening)": 0}

application_mode_map = {
    "Fase 1 - Kontingensi Umum": 1,
    "Ordinance No. 612/93": 2,
    "Fase 1 - Kontingensi Khusus (Pulau Azores)": 5,
    "Pemegang Kursus Tinggi Lainnya": 7,
    "Ordinance No. 854-B/99": 10,
    "Mahasiswa Internasional (Sarjana)": 15,
    "Fase 1 - Kontingensi Khusus (Pulau Madeira)": 16,
    "Fase 2 - Kontingensi Umum": 17,
    "Fase 3 - Kontingensi Umum": 18,
    "Ordinance No. 533-A/99, item b2 (Rencana Berbeda)": 26,
    "Ordinance No. 533-A/99, item b3 (Institusi Lain)": 27,
    "Usia di atas 23 tahun": 39,
    "Transfer": 42,
    "Perubahan Program Studi": 43,
    "Pemegang Diploma Spesialisasi Teknologi": 44,
    "Perubahan Institusi/Program Studi": 51,
    "Pemegang Diploma Siklus Singkat": 53,
    "Perubahan Institusi/Program Studi (Internasional)": 57,
}

course_map = {
    "Biofuel Production Technologies": 33,
    "Animation and Multimedia Design": 171,
    "Social Service (evening)": 8014,
    "Agronomy": 9003,
    "Communication Design": 9070,
    "Veterinary Nursing": 9085,
    "Informatics Engineering": 9119,
    "Equinculture": 9130,
    "Management": 9147,
    "Social Service": 9238,
    "Tourism": 9254,
    "Nursing": 9500,
    "Oral Hygiene": 9556,
    "Advertising and Marketing Management": 9670,
    "Journalism and Communication": 9773,
    "Basic Education": 9853,
    "Management (evening)": 9991,
}

previous_qualification_map = {
    "Pendidikan Menengah (SMA)": 1,
    "Pendidikan Tinggi - Bachelor": 2,
    "Pendidikan Tinggi - Degree": 3,
    "Pendidikan Tinggi - Master": 4,
    "Pendidikan Tinggi - Doktor": 5,
    "Sedang Menempuh Pendidikan Tinggi": 6,
    "Kelas 12 - Tidak Selesai": 9,
    "Kelas 11 - Tidak Selesai": 10,
    "Lainnya - Kelas 11": 12,
    "Kelas 10": 14,
    "Kelas 10 - Tidak Selesai": 15,
    "Pendidikan Dasar Siklus 3 (Kelas 9-11)": 19,
    "Pendidikan Dasar Siklus 2 (Kelas 6-8)": 38,
    "Kursus Spesialisasi Teknologi": 39,
    "Pendidikan Tinggi - Degree (Siklus 1)": 40,
    "Kursus Teknik Tinggi Profesional": 42,
    "Pendidikan Tinggi - Master (Siklus 2)": 43,
}

nacionality_map = {
    "Portugis": 1, "Jerman": 2, "Spanyol": 6, "Italia": 11, "Belanda": 13,
    "Inggris": 14, "Lituania": 17, "Angola": 21, "Cape Verde": 22, "Guinea": 24,
    "Mozambik": 25, "Sao Tome": 26, "Turki": 32, "Brasil": 41, "Rumania": 62,
    "Moldova": 100, "Meksiko": 101, "Ukraina": 103, "Rusia": 105, "Kuba": 108,
    "Kolombia": 109,
}

parent_qualification_map = {
    "Pendidikan Menengah (Kelas 12)": 1,
    "Pendidikan Tinggi - Bachelor": 2,
    "Pendidikan Tinggi - Degree": 3,
    "Pendidikan Tinggi - Master": 4,
    "Pendidikan Tinggi - Doktor": 5,
    "Sedang Menempuh Pendidikan Tinggi": 6,
    "Kelas 12 - Tidak Selesai": 9,
    "Kelas 11 - Tidak Selesai": 10,
    "Kelas 7 (Lama)": 11,
    "Lainnya - Kelas 11": 12,
    "Kelas 10": 14,
    "Kursus Perdagangan Umum": 18,
    "Pendidikan Dasar Siklus 3 (Kelas 9-11)": 19,
    "Kursus Teknik-Profesional": 22,
    "Kelas 7": 26,
    "Sekolah Menengah Umum Siklus 2": 27,
    "Kelas 9 - Tidak Selesai": 29,
    "Kelas 8": 30,
    "Tidak Diketahui": 34,
    "Tidak Bisa Baca Tulis": 35,
    "Bisa Membaca tanpa Kelas 4": 36,
    "Pendidikan Dasar Siklus 1 (Kelas 4-5)": 37,
    "Pendidikan Dasar Siklus 2 (Kelas 6-8)": 38,
    "Kursus Spesialisasi Teknologi": 39,
    "Pendidikan Tinggi - Degree (Siklus 1)": 40,
    "Studi Tinggi Terspesialisasi": 41,
    "Kursus Teknik Tinggi Profesional": 42,
    "Pendidikan Tinggi - Master (Siklus 2)": 43,
    "Pendidikan Tinggi - Doktor (Siklus 3)": 44,
}

occupation_map = {
    "Pelajar": 0,
    "Pejabat Legislatif/Eksekutif, Direktur, Manajer Eksekutif": 1,
    "Spesialis Kegiatan Intelektual dan Ilmiah": 2,
    "Teknisi dan Profesi Tingkat Menengah": 3,
    "Staf Administratif": 4,
    "Pekerja Layanan Personal, Keamanan, dan Penjual": 5,
    "Petani dan Pekerja Terampil Pertanian/Perikanan/Kehutanan": 6,
    "Pekerja Terampil Industri, Konstruksi, dan Pengrajin": 7,
    "Operator Instalasi dan Mesin, Pekerja Perakitan": 8,
    "Pekerja Tidak Terampil": 9,
    "Profesi Angkatan Bersenjata": 10,
    "Situasi Lainnya": 90,
    "Tidak Diketahui / Kosong": 99,
    "Petugas Angkatan Bersenjata": 101,
    "Sersan Angkatan Bersenjata": 102,
    "Personel Angkatan Bersenjata Lainnya": 103,
    "Direktur Layanan Administratif dan Komersial": 112,
    "Direktur Hotel, Katering, Perdagangan, dan Layanan Lain": 114,
    "Spesialis Sains Fisika, Matematika, Teknik": 121,
    "Profesional Kesehatan": 122,
    "Guru/Pengajar": 123,
    "Spesialis Keuangan, Akuntansi, Administrasi": 124,
    "Spesialis Teknologi Informasi dan Komunikasi (ICT)": 125,
    "Teknisi Sains dan Teknik Tingkat Menengah": 131,
    "Teknisi Kesehatan Tingkat Menengah": 132,
    "Teknisi Hukum, Sosial, Olahraga, Budaya Tingkat Menengah": 134,
    "Teknisi Teknologi Informasi dan Komunikasi": 135,
    "Pekerja Kantor, Sekretaris, Operator Data": 141,
    "Operator Layanan Data, Akuntansi, Keuangan, Registri": 143,
    "Staf Pendukung Administratif Lainnya": 144,
    "Pekerja Layanan Personal": 151,
    "Penjual": 152,
    "Pekerja Perawatan Personal": 153,
    "Personel Layanan Perlindungan dan Keamanan": 154,
    "Petani Berorientasi Pasar dan Pekerja Peternakan Terampil": 161,
    "Petani/Peternak/Nelayan Subsisten": 163,
    "Pekerja Konstruksi Terampil (Kecuali Listrik)": 171,
    "Pekerja Terampil Metalurgi dan Sejenisnya": 172,
    "Pekerja Terampil Percetakan, Instrumen Presisi, Kerajinan": 173,
    "Pekerja Terampil Listrik dan Elektronik": 174,
    "Pekerja Pengolahan Makanan, Kayu, Pakaian, Kerajinan": 175,
    "Operator Mesin dan Instalasi Tetap": 181,
    "Pekerja Perakitan": 182,
    "Pengemudi Kendaraan dan Operator Alat Berat": 183,
    "Pekerja Kebersihan": 191,
    "Pekerja Tidak Terampil Pertanian/Peternakan/Perikanan": 192,
    "Pekerja Tidak Terampil Industri Ekstraktif/Konstruksi/Transportasi": 193,
    "Asisten Persiapan Makanan": 194,
    "Pedagang Kaki Lima dan Penyedia Layanan Jalanan": 195,
}

# ============================================================
# ==== FORM INPUT ====
# ============================================================

with st.form("prediction_form"):

    st.subheader("Data Demografi")
    col1, col2 = st.columns(2)
    with col1:
        marital_status = st.selectbox("Status Pernikahan", list(marital_map.keys()))
        gender = st.selectbox("Jenis Kelamin", list(gender_map.keys()))
        age_at_enrollment = st.number_input("Usia saat Mendaftar", min_value=15, max_value=70, value=20)
        nacionality = st.selectbox("Kewarganegaraan", list(nacionality_map.keys()))
    with col2:
        displaced = st.selectbox("Pindah Domisili untuk Kuliah", list(yes_no_map.keys()))
        international = st.selectbox("Mahasiswa Internasional", list(yes_no_map.keys()))
        educational_special_needs = st.selectbox("Kebutuhan Khusus Pendidikan", list(yes_no_map.keys()))

    st.subheader("Data Pendaftaran & Akademik")
    col3, col4 = st.columns(2)
    with col3:
        course = st.selectbox("Program Studi", list(course_map.keys()))
        daytime_evening = st.selectbox("Waktu Perkuliahan", list(attendance_map.keys()))
        application_mode = st.selectbox("Jalur Pendaftaran", list(application_mode_map.keys()))
        application_order = st.selectbox("Urutan Pilihan Program Studi", list(range(0, 10)),
                                          help="0 = pilihan pertama, 9 = pilihan terakhir")
    with col4:
        previous_qualification = st.selectbox("Kualifikasi Pendidikan Sebelumnya", list(previous_qualification_map.keys()))
        previous_qualification_grade = st.number_input("Nilai Kualifikasi Sebelumnya (skala 0-200)", min_value=0.0, max_value=200.0, value=120.0)
        admission_grade = st.number_input("Nilai Penerimaan (skala 0-200)", min_value=0.0, max_value=200.0, value=120.0)

    st.subheader("Latar Belakang Keluarga")
    col5, col6 = st.columns(2)
    with col5:
        mothers_qualification = st.selectbox("Pendidikan Terakhir Ibu", list(parent_qualification_map.keys()))
        mothers_occupation = st.selectbox("Pekerjaan Ibu", list(occupation_map.keys()))
    with col6:
        fathers_qualification = st.selectbox("Pendidikan Terakhir Ayah", list(parent_qualification_map.keys()))
        fathers_occupation = st.selectbox("Pekerjaan Ayah", list(occupation_map.keys()))

    st.subheader("Kondisi Sosial-Ekonomi")
    col7, col8 = st.columns(2)
    with col7:
        debtor = st.selectbox("Memiliki Tunggakan (Debitur)", list(yes_no_map.keys()))
        tuition_fees = st.selectbox("Uang Kuliah Lunas", list(yes_no_map.keys()))
    with col8:
        scholarship_holder = st.selectbox("Penerima Beasiswa", list(yes_no_map.keys()))

    st.subheader("Performa Akademik Semester 1")
    col9, col10, col11 = st.columns(3)
    with col9:
        cu1_credited = st.number_input("SKS Diakui", min_value=0, max_value=30, value=0, key="cu1_credited")
        cu1_enrolled = st.number_input("SKS Diambil", min_value=0, max_value=30, value=6, key="cu1_enrolled")
    with col10:
        cu1_evaluations = st.number_input("Jumlah Evaluasi", min_value=0, max_value=50, value=6, key="cu1_eval")
        cu1_approved = st.number_input("SKS Lulus", min_value=0, max_value=30, value=5, key="cu1_approved")
    with col11:
        cu1_grade = st.number_input("Rata-rata Nilai (skala 0-20)", min_value=0.0, max_value=20.0, value=12.0, key="cu1_grade")
        cu1_without_eval = st.number_input("Tanpa Evaluasi", min_value=0, max_value=30, value=0, key="cu1_woeval")

    st.subheader("Performa Akademik Semester 2")
    col12, col13, col14 = st.columns(3)
    with col12:
        cu2_credited = st.number_input("SKS Diakui", min_value=0, max_value=30, value=0, key="cu2_credited")
        cu2_enrolled = st.number_input("SKS Diambil", min_value=0, max_value=30, value=6, key="cu2_enrolled")
    with col13:
        cu2_evaluations = st.number_input("Jumlah Evaluasi", min_value=0, max_value=50, value=6, key="cu2_eval")
        cu2_approved = st.number_input("SKS Lulus", min_value=0, max_value=30, value=5, key="cu2_approved")
    with col14:
        cu2_grade = st.number_input("Rata-rata Nilai (skala 0-20)", min_value=0.0, max_value=20.0, value=12.0, key="cu2_grade")
        cu2_without_eval = st.number_input("Tanpa Evaluasi", min_value=0, max_value=30, value=0, key="cu2_woeval")

    st.subheader("Indikator Makroekonomi")
    st.caption("Kondisi ekonomi nasional pada saat siswa terdaftar")
    col15, col16, col17 = st.columns(3)
    with col15:
        unemployment_rate = st.number_input("Tingkat Pengangguran (%)", value=10.0)
    with col16:
        inflation_rate = st.number_input("Tingkat Inflasi (%)", value=1.0)
    with col17:
        gdp = st.number_input("GDP", value=0.0)

    submitted = st.form_submit_button("Prediksi Status Siswa")

# ============================================================
# ==== PROSES PREDIKSI ====
# ============================================================

if submitted:
    input_data = pd.DataFrame([{
        'Marital_status': marital_map[marital_status],
        'Application_mode': application_mode_map[application_mode],
        'Application_order': application_order,
        'Course': course_map[course],
        'Daytime_evening_attendance': attendance_map[daytime_evening],
        'Previous_qualification': previous_qualification_map[previous_qualification],
        'Previous_qualification_grade': previous_qualification_grade,
        'Nacionality': nacionality_map[nacionality],
        'Mothers_qualification': parent_qualification_map[mothers_qualification],
        'Fathers_qualification': parent_qualification_map[fathers_qualification],
        'Mothers_occupation': occupation_map[mothers_occupation],
        'Fathers_occupation': occupation_map[fathers_occupation],
        'Admission_grade': admission_grade,
        'Displaced': yes_no_map[displaced],
        'Educational_special_needs': yes_no_map[educational_special_needs],
        'Debtor': yes_no_map[debtor],
        'Tuition_fees_up_to_date': yes_no_map[tuition_fees],
        'Gender': gender_map[gender],
        'Scholarship_holder': yes_no_map[scholarship_holder],
        'Age_at_enrollment': age_at_enrollment,
        'International': yes_no_map[international],
        'Curricular_units_1st_sem_credited': cu1_credited,
        'Curricular_units_1st_sem_enrolled': cu1_enrolled,
        'Curricular_units_1st_sem_evaluations': cu1_evaluations,
        'Curricular_units_1st_sem_approved': cu1_approved,
        'Curricular_units_1st_sem_grade': cu1_grade,
        'Curricular_units_1st_sem_without_evaluations': cu1_without_eval,
        'Curricular_units_2nd_sem_credited': cu2_credited,
        'Curricular_units_2nd_sem_enrolled': cu2_enrolled,
        'Curricular_units_2nd_sem_evaluations': cu2_evaluations,
        'Curricular_units_2nd_sem_approved': cu2_approved,
        'Curricular_units_2nd_sem_grade': cu2_grade,
        'Curricular_units_2nd_sem_without_evaluations': cu2_without_eval,
        'Unemployment_rate': unemployment_rate,
        'Inflation_rate': inflation_rate,
        'GDP': gdp,
    }])

    prediction = model.predict(input_data)
    prediction_label = label_encoder.inverse_transform(prediction)[0]

    proba = model.predict_proba(input_data)[0]
    proba_dict = dict(zip(label_encoder.classes_, proba))

    st.divider()
    st.subheader("Hasil Prediksi")

    card_class = {
        "Dropout": "result-dropout",
        "Enrolled": "result-enrolled",
        "Graduate": "result-graduate"
    }[prediction_label]

    status_label_id = {
        "Dropout": "Dropout",
        "Enrolled": "Masih Aktif Kuliah",
        "Graduate": "Lulus"
    }[prediction_label]

    desc_text = {
        "Dropout": "Siswa ini terindikasi berisiko dropout. Disarankan mendapat bimbingan akademik dan/atau finansial secepatnya.",
        "Enrolled": "Siswa ini diprediksi masih akan aktif berkuliah pada periode evaluasi berikutnya.",
        "Graduate": "Siswa ini diprediksi akan menyelesaikan studinya dengan baik."
    }[prediction_label]

    st.markdown(f"""
    <div class="result-card {card_class}">
        <div class="result-title">STATUS PREDIKSI</div>
        <div class="result-status">{status_label_id}</div>
        <div class="result-desc">{desc_text}</div>
    </div>
    """, unsafe_allow_html=True)

    color_map = {"Dropout": "#c0392b", "Enrolled": "#2e5aac", "Graduate": "#27ae60"}

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.write("Distribusi probabilitas tiap status")
        proba_df = pd.DataFrame({
            "Status": list(proba_dict.keys()),
            "Probabilitas": list(proba_dict.values())
        }).sort_values("Probabilitas", ascending=False)

        fig, ax = plt.subplots(figsize=(5, 3))
        colors = [color_map[s] for s in proba_df["Status"]]
        ax.bar(proba_df["Status"], proba_df["Probabilitas"], color=colors)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Probabilitas")
        for i, v in enumerate(proba_df["Probabilitas"]):
            ax.text(i, v + 0.02, f"{v*100:.1f}%", ha='center', fontsize=9)
        st.pyplot(fig)

    with col_b:
        for status, p in sorted(proba_dict.items(), key=lambda x: -x[1]):
            st.metric(status, f"{p*100:.1f}%")