import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load('model/model_rf.joblib')
label_encoder = joblib.load('model/label_encoder.joblib')

st.set_page_config(page_title="Prediksi Status Siswa - Jaya Jaya Institut", layout="centered")

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
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 6px solid;
    }
    .result-dropout { background-color: #fdecea; border-color: #c0392b; }
    .result-enrolled { background-color: #eaf2fb; border-color: #2e5aac; }
    .result-graduate { background-color: #eafaf1; border-color: #27ae60; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Prediksi Status Siswa")
st.markdown("""
Aplikasi ini membantu Jaya Jaya Institut memprediksi kemungkinan status siswa
(**Dropout**, **Enrolled**, atau **Graduate**) berdasarkan data demografi,
sosial-ekonomi, dan performa akademik siswa.
""")

st.divider()

marital_map = {
    "Single": 1, "Married": 2, "Widower": 3,
    "Divorced": 4, "Facto Union": 5, "Legally Separated": 6
}
gender_map = {"Laki-laki": 1, "Perempuan": 0}
yes_no_map = {"Ya": 1, "Tidak": 0}
attendance_map = {"Siang (Daytime)": 1, "Malam (Evening)": 0}

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

# ==== Form input ====
with st.form("prediction_form"):

    st.subheader("Data Demografi")
    col1, col2 = st.columns(2)
    with col1:
        marital_status = st.selectbox("Status Pernikahan", list(marital_map.keys()))
        gender = st.selectbox("Jenis Kelamin", list(gender_map.keys()))
        age_at_enrollment = st.number_input("Usia saat Mendaftar", min_value=15, max_value=70, value=20)
    with col2:
        displaced = st.selectbox("Status Displaced (pindah domisili)", list(yes_no_map.keys()))
        international = st.selectbox("Mahasiswa Internasional", list(yes_no_map.keys()))
        educational_special_needs = st.selectbox("Kebutuhan Khusus Pendidikan", list(yes_no_map.keys()))

    st.subheader("Data Akademik & Pendaftaran")
    col3, col4 = st.columns(2)
    with col3:
        course = st.selectbox("Program Studi", list(course_map.keys()))
        daytime_evening = st.selectbox("Waktu Perkuliahan", list(attendance_map.keys()))
        application_mode = st.number_input("Kode Application Mode", min_value=1, max_value=60, value=1,
                                            help="Lihat kode lengkap pada dokumentasi dataset")
        application_order = st.number_input("Urutan Pilihan (0=pilihan pertama)", min_value=0, max_value=9, value=1)
    with col4:
        previous_qualification = st.number_input("Kode Kualifikasi Sebelumnya", min_value=1, max_value=43, value=1)
        previous_qualification_grade = st.number_input("Nilai Kualifikasi Sebelumnya (0-200)", min_value=0.0, max_value=200.0, value=120.0)
        admission_grade = st.number_input("Nilai Penerimaan (0-200)", min_value=0.0, max_value=200.0, value=120.0)
        nacionality = st.number_input("Kode Kewarganegaraan", min_value=1, max_value=110, value=1)

    st.subheader("Latar Belakang Keluarga")
    col5, col6 = st.columns(2)
    with col5:
        mothers_qualification = st.number_input("Kode Kualifikasi Ibu", min_value=1, max_value=44, value=1)
        mothers_occupation = st.number_input("Kode Pekerjaan Ibu", min_value=0, max_value=194, value=1)
    with col6:
        fathers_qualification = st.number_input("Kode Kualifikasi Ayah", min_value=1, max_value=44, value=1)
        fathers_occupation = st.number_input("Kode Pekerjaan Ayah", min_value=0, max_value=195, value=1)

    st.subheader("Kondisi Sosial-Ekonomi")
    col7, col8 = st.columns(2)
    with col7:
        debtor = st.selectbox("Status Debitur (punya tunggakan)", list(yes_no_map.keys()))
        tuition_fees = st.selectbox("Uang Kuliah Lunas", list(yes_no_map.keys()))
    with col8:
        scholarship_holder = st.selectbox("Penerima Beasiswa", list(yes_no_map.keys()))

    st.subheader("Performa Akademik Semester 1")
    col9, col10, col11 = st.columns(3)
    with col9:
        cu1_credited = st.number_input("SKS Diakui (Sem 1)", min_value=0, max_value=30, value=0)
        cu1_enrolled = st.number_input("SKS Diambil (Sem 1)", min_value=0, max_value=30, value=6)
    with col10:
        cu1_evaluations = st.number_input("Jumlah Evaluasi (Sem 1)", min_value=0, max_value=50, value=6)
        cu1_approved = st.number_input("SKS Lulus (Sem 1)", min_value=0, max_value=30, value=5)
    with col11:
        cu1_grade = st.number_input("Rata-rata Nilai (Sem 1)", min_value=0.0, max_value=20.0, value=12.0)
        cu1_without_eval = st.number_input("Tanpa Evaluasi (Sem 1)", min_value=0, max_value=30, value=0)

    st.subheader("Performa Akademik Semester 2")
    col12, col13, col14 = st.columns(3)
    with col12:
        cu2_credited = st.number_input("SKS Diakui (Sem 2)", min_value=0, max_value=30, value=0)
        cu2_enrolled = st.number_input("SKS Diambil (Sem 2)", min_value=0, max_value=30, value=6)
    with col13:
        cu2_evaluations = st.number_input("Jumlah Evaluasi (Sem 2)", min_value=0, max_value=50, value=6)
        cu2_approved = st.number_input("SKS Lulus (Sem 2)", min_value=0, max_value=30, value=5)
    with col14:
        cu2_grade = st.number_input("Rata-rata Nilai (Sem 2)", min_value=0.0, max_value=20.0, value=12.0)
        cu2_without_eval = st.number_input("Tanpa Evaluasi (Sem 2)", min_value=0, max_value=30, value=0)

    st.subheader("Indikator Makroekonomi")
    col15, col16, col17 = st.columns(3)
    with col15:
        unemployment_rate = st.number_input("Tingkat Pengangguran (%)", value=10.0)
    with col16:
        inflation_rate = st.number_input("Tingkat Inflasi (%)", value=1.0)
    with col17:
        gdp = st.number_input("GDP", value=0.0)

    submitted = st.form_submit_button("🔍 Prediksi Status Siswa")

# ==== Proses prediksi ====
if submitted:
    input_data = pd.DataFrame([{
        'Marital_status': marital_map[marital_status],
        'Application_mode': application_mode,
        'Application_order': application_order,
        'Course': course_map[course],
        'Daytime_evening_attendance': attendance_map[daytime_evening],
        'Previous_qualification': previous_qualification,
        'Previous_qualification_grade': previous_qualification_grade,
        'Nacionality': nacionality,
        'Mothers_qualification': mothers_qualification,
        'Fathers_qualification': fathers_qualification,
        'Mothers_occupation': mothers_occupation,
        'Fathers_occupation': fathers_occupation,
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

    if prediction_label == "Dropout":
        st.error(f"⚠️ Prediksi Status: **{prediction_label}**")
        st.warning("Siswa ini terindikasi berisiko dropout. Disarankan untuk diberikan bimbingan khusus.")
    elif prediction_label == "Enrolled":
        st.info(f"📘 Prediksi Status: **{prediction_label}**")
    else:
        st.success(f"🎓 Prediksi Status: **{prediction_label}**")

    st.write("Probabilitas tiap kelas:")
    proba_df = pd.DataFrame(proba_dict.items(), columns=["Status", "Probabilitas"]).sort_values("Probabilitas", ascending=False)
    st.bar_chart(proba_df.set_index("Status"))