# Menyelesaikan Permasalahan Institusi Pendidikan (Jaya Jaya Institut)

## Business Understanding

Jaya Jaya Institut merupakan institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000 dan sejauh ini telah mencetak banyak lulusan dengan reputasi baik. Namun di balik pencapaian tersebut, institusi ini masih menghadapi masalah serius: tingginya angka siswa yang tidak menyelesaikan pendidikannya alias dropout. Bagi sebuah institusi pendidikan, tingkat dropout yang tinggi bukan hanya soal angka, tapi berdampak langsung pada reputasi institusi, efisiensi biaya operasional, serta yang paling penting, masa depan siswa itu sendiri.

Saat ini pihak institusi baru bisa mengetahui siswa berisiko dropout setelah kondisinya sudah cukup parah, sehingga bimbingan khusus yang diberikan seringkali terlambat. Proyek ini bertujuan membantu Jaya Jaya Institut membangun sebuah sistem yang dapat mendeteksi potensi dropout siswa sedini mungkin, berdasarkan data yang mereka miliki sejak siswa mendaftar hingga performa akademik semester awal.

### Permasalahan Bisnis

Berdasarkan latar belakang di atas, permasalahan yang dijawab dalam proyek ini adalah:
- Faktor apa saja yang paling berpengaruh terhadap potensi dropout siswa di Jaya Jaya Institut?
- Bagaimana cara memprediksi status siswa (Dropout, Enrolled, atau Graduate) berdasarkan data demografi, sosial-ekonomi, dan performa akademik mereka?
- Bagaimana pihak institusi dapat memonitor performa siswa secara berkelanjutan agar bisa memberikan intervensi lebih cepat?

### Cakupan Proyek

Untuk menjawab permasalahan tersebut, ruang lingkup proyek ini meliputi:
1. Melakukan eksplorasi data (EDA) untuk memahami karakteristik dan pola pada data siswa.
2. Melakukan data preparation agar data siap digunakan untuk pemodelan.
3. Membangun model machine learning untuk mengklasifikasikan status siswa ke dalam tiga kategori: Dropout, Enrolled, dan Graduate.
4. Mengevaluasi performa model yang dibangun.
5. Membuat business dashboard untuk membantu pihak institusi memonitor performa dan faktor risiko siswa.
6. Membangun prototype sistem prediksi berbasis Streamlit dan men-deploy-nya agar dapat diakses secara online.

### Persiapan

Sumber data: dataset "Students' Performance" yang disediakan oleh Jaya Jaya Institut melalui Dicoding.

Setup environment:

```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
```

Menjalankan notebook:

```bash
jupyter notebook notebook.ipynb
```

## Business Dashboard

Dashboard ini dibangun menggunakan Looker Studio dan menyajikan gambaran menyeluruh mengenai performa dan faktor risiko dropout siswa di Jaya Jaya Institut, meliputi:
- Ringkasan jumlah total siswa, jumlah siswa dropout, dan persentase dropout
- Komposisi status siswa (Dropout, Enrolled, Graduate)
- Hubungan status pembayaran uang kuliah terhadap status siswa
- Hubungan status penerima beasiswa terhadap status siswa
- Rata-rata nilai akademik semester 2 per status siswa
- Tingkat dropout per program studi
- Filter interaktif berdasarkan program studi

Link dashboard: [Dashboard Monitoring Performa Siswa - Jaya Jaya Institut](https://datastudio.google.com/reporting/2fdfd7b6-32ed-4c8a-aaaa-14a0a6f7bc1b)

**Insight utama dari dashboard:**
1. Siswa yang belum melunasi uang kuliah menunjukkan proporsi dropout yang jauh lebih tinggi dibanding siswa yang sudah lunas, yang menandakan hal ini merupakan risiko paling kuat yang ditemukan dalam data.
2. Rata-rata nilai semester 2 siswa dengan status Dropout jauh lebih rendah dibanding Enrolled maupun Graduate, sebagian besar disebabkan oleh siswa yang keluar sebelum sempat dievaluasi pada semester tersebut.
3. Beberapa program studi memiliki tingkat dropout yang signifikan lebih tinggi dibanding rata-rata keseluruhan, sehingga membutuhkan perhatian dan intervensi yang lebih spesifik.

## Menjalankan Sistem Machine Learning

Prototype sistem prediksi dropout siswa dibangun menggunakan Streamlit dan telah di-deploy ke Streamlit Community Cloud sehingga dapat diakses secara online tanpa perlu instalasi apa pun.

Link prototype: https://dropout-prediction-jja-kcvs7kkw4k33cdb558uj8u.streamlit.app/

Cara menjalankan secara lokal:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Model yang digunakan pada prototype ini adalah **Random Forest Classifier** dengan parameter `class_weight='balanced'`, yang dipilih berdasarkan hasil evaluasi pada notebook (lihat bagian Evaluation di `notebook.ipynb`) karena memberikan keseimbangan terbaik antara kemampuan mendeteksi siswa Dropout dan siswa Enrolled dibandingkan varian model lain yang diuji.

## Conclusion

Berdasarkan seluruh proses yang telah dilakukan, ditemukan bahwa status pembayaran uang kuliah dan performa akademik pada semester 1 dan 2 (jumlah mata kuliah yang disetujui serta nilai rata-rata) merupakan faktor paling berpengaruh terhadap potensi dropout siswa di Jaya Jaya Institut. Siswa yang belum melunasi uang kuliah menunjukkan proporsi dropout yang jauh lebih tinggi dibanding siswa yang sudah lunas.

Model Random Forest dengan `class_weight='balanced'` yang dipilih sebagai model final mampu mengklasifikasikan status siswa dengan macro average recall sebesar 0.71, dengan kemampuan mendeteksi siswa Dropout pada recall 0.71 dan presisi 0.83. Model ini menjawab permasalahan bisnis yang diajukan Jaya Jaya Institut, yaitu mendeteksi siswa berisiko dropout sedini mungkin agar dapat diberikan bimbingan khusus lebih cepat.

Model ini masih memiliki keterbatasan dalam mengklasifikasikan siswa dengan status Enrolled, yang kemungkinan disebabkan oleh karakteristik data siswa aktif yang berada di antara pola siswa Dropout dan Graduate. Hal ini menjadi catatan bagi pengembangan model di masa mendatang.

### Rekomendasi Action Items

Berdasarkan temuan pada tahap analisis dan pemodelan, berikut rekomendasi konkret yang dapat dilakukan oleh Jaya Jaya Institut:

- **Prioritaskan intervensi finansial di awal semester.** Karena status pembayaran uang kuliah adalah sinyal risiko dropout terkuat, institusi sebaiknya membangun sistem peringatan dini bagi siswa yang menunggak, disertai opsi keringanan atau skema cicilan sebelum siswa memutuskan berhenti.
- **Pantau performa akademik semester 1 secara aktif**, bukan hanya di akhir semester. Siswa dengan jumlah mata kuliah lulus yang rendah pada semester pertama sebaiknya langsung mendapat pendampingan akademik (mentoring/tutoring) tanpa menunggu semester berikutnya.
- **Berikan perhatian khusus pada program studi dengan tingkat dropout tertinggi** (dapat dilihat pada dashboard) melalui evaluasi kurikulum, beban studi, atau dukungan tambahan yang disesuaikan dengan karakteristik program studi tersebut.
- **Perluas cakupan program beasiswa** pada kelompok siswa yang menunjukkan tekanan finansial, karena data menunjukkan siswa penerima beasiswa memiliki proporsi kelulusan yang lebih baik.
- **Gunakan prototype sistem prediksi ini sebagai alat bantu rutin** bagi bagian akademik/kemahasiswaan untuk melakukan skrining awal terhadap siswa baru maupun siswa aktif, sehingga bimbingan dapat diberikan secara proaktif, bukan reaktif.
- **Lakukan evaluasi ulang model secara berkala** (misalnya setiap tahun ajaran) menggunakan data terbaru, mengingat pola dropout siswa dapat berubah seiring waktu dan kondisi eksternal seperti kondisi ekonomi.