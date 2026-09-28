Nama : Yosua Peitho Purba
NPM : 2506657402
Kelas : PBP D

### Tugas 1

1. Penggunaan Elemen Semantik HTML5
Ya, saya menggunakan elemen semantik HTML5 seperti <header>, <main>, <section>, dan <footer> dalam merancang struktur kode HTML dalam portofolio ini. Elemen-elemen ini sangat membantu dalam membuat *static web* karena membuat struktur kode menjadi jauh lebih bersih, terorganisir, dan mudah dibaca (*readable*). Selain itu, penggunaan elemen semantik memberikan konteks yang jelas bagi mesin pencari (*SEO*) dan pembaca layar (*accessibility*), sehingga bagian identitas utama, bagian pengalaman (*experience*), hingga bagian keahlian (*skills*) terisolasi dengan logis di dalam dokumen.

2. Tantangan utama dalam menjaga portofolio tetap responsif adalah mengatur proporsi tata letak elemen *Hero* yang memiliki grid yang tidak simetris antara teks identitas, detail informasi, dan foto profil, agar tidak berantakan saat beralih ke layar kecil (*mobile*). Untuk mengevaluasinya, saya memprioritaskan keterbacaan konten utama dan konsistensi hierarki visual terlebih dahulu. Ketika beralih dari *desktop* ke *mobile*, saya menggunakan *media queries* dengan mengubah struktur *grid-template-areas* serta mengatur ulang lebar elemen menggunakan unit relatif dan *flex-direction: column*, sehingga foto profil dan informasi teks dapat tersusun secara vertikal dengan rapi tanpa terpotong.

3. Sebagai *static web* murni, batasannya terletak pada interaktivitas yang terbatas; informasi bersifat kaku (*hardcoded*), tidak ada penyimpanan basis data (*database*), dan tidak ada fitur umpan balik langsung seperti formulir kontak yang dapat memproses pesan secara *real-time*. Berdasarkan batasan tersebut, fungsionalitas dinamis yang ingin saya tambahkan pada iterasi proyek selanjutnya adalah sistem manajemen konten (CMS) berbasis Django untuk mengelola daftar proyek atau *experience* secara dinamis melalui halaman *admin*, serta integrasi *contact form* interaktif yang dilengkapi validasi sisi server dan sistem pengiriman email otomatis.

### Tugas 2

1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.
**Alur Request-Response**:
  **Browser** mengirimkan permintaan HTTP GET ketika pengguna mengakses URL tertentu (misal: `/education/`).
  **`urls.py` Proyek**: Menerima request pertama kali dan mencocokkan awalan URL, lalu meneruskannya (*include*) ke `urls.py` milik aplikasi terkait.
  **`urls.py` Aplikasi**: Mencocokkan rute spesifik yang diminta dan memanggil fungsi **View** yang sesuai.
  **View**: Memproses logika bisnis. View akan meminta data yang dibutuhkan dari **Model**.
  **Model**: Mengambil atau memproses data dari database SQLite dan mengembalikannya ke View dalam bentuk objek/QuerySet.
  **View**: Menggabungkan data dari Model dengan berkas **Template** (HTML) menggunakan *context dictionary*.
  **Template**: Mengolah tag-tag Django HTML (seperti `{% for %}`) menjadi kode HTML murni yang berisi data dinamis.
  **Response**: View mengembalikan hasil rendering HTML tersebut sebagai `HttpResponse` ke browser pengguna untuk ditampilkan.

2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.
    **Pemisahan Logika & Data (*Separation of Concerns*)**: Menimpan data di Model menjaga berkas HTML (Template) tetap bersih dan hanya berfokus pada struktur tampilan/UI.
    **Kemudahan Pemeliharaan (*Maintainability*)**: Jika ada perubahan data (seperti menambah riwayat pendidikan baru), kita cukup mengeditnya lewat database/form tanpa perlu menyentuh atau merusak struktur kode HTML.
    **Skalabilitas & Dinamis**: Data yang ada di Model dapat diakses kembali oleh berbagai fitur lain, seperti disajikan dalam format JSON/XML API, difilter lewat pencarian, atau dihubungkan dengan fitur autentikasi pengguna.

3. Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.
    **Perbedaan**:
    **`makemigrations`**: Bertugas mendeteksi perubahan pada berkas `models.py` dan membuat berkas skrip migrasi baru (misal: `0002_education.py`) di dalam folder `migrations/`. Perintah ini **belum** mengubah struktur database.
    **`migrate`**: Eksekutor yang menjalankan skrip migrasi yang telah dibuat tadi ke database fisik (seperti SQLite), sehingga tabel dan kolom database mengalami perubahan secara riil.
    **Contoh Perubahan Model**: 
        Saat menambahkan model baru `Education` atau menambah field baru seperti `degree = models.CharField(max_length=255)` pada model yang sudah ada. Kedua perintah wajib dijalankan berturut-turut agar tabel database menyesuaikan struktur model baru tersebut.

### Tugas 3

1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!
**Alasan Menggunakan ModelForm**:
    `ModelForm` secara otomatis membangun bidang-bidang form (*form fields*) berdasarkan struktur model yang ada di Django. Hal ini memangkas pengulangan kode secara signifikan (*Don't Repeat Yourself*), mengotomatiskan proses validasi data sesuai tipe dan aturan pada model, serta memungkinkan kita menyimpan data dari input pengguna langsung ke database hanya dengan memanggil `form.save()`.
**Alasan Kewajiban `{% csrf_token %}`**:
    Tag `{% csrf_token %}` menghasilkan token unik dan rahasia yang berfungsi untuk melindungi aplikasi dari serangan **CSRF (Cross-Site Request Forgery)**. Token ini memastikan bahwa setiap permintaan `POST` yang masuk benar-benar berasal dari pengguna sah yang sedang berinteraksi di situs kita, bukan dari situs web pihak ketiga yang berbahaya.

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
**Sintaks Ringkas dan Ukuran Lebih Kecil**: JSON menggunakan format pasangan *key-value* yang jauh lebih sederhana dibandingkan XML yang memerlukan tag pembuka dan penutup untuk setiap elemen. Hal ini membuat payload data JSON lebih ringan dan lebih cepat dikirimkan melalui jaringan.
**Integrasi Native dengan JavaScript**: JSON (*JavaScript Object Notation*) dapat langsung dibaca dan diolah secara *native* oleh JavaScript di browser tanpa memerlukan *DOM Parser* khusus seperti halnya XML, sehingga sangat cocok untuk ekosistem *frontend* modern (React, Vue, Fetch API).
**Kemudahan Pembacaan**: Struktur data JSON lebih intuitif dan mudah dibaca oleh pengembang (*human-readable*).

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
    **Alur Proses Pembentukan Response JSON**:
  - *Client* (browser/Postman) mengirimkan permintaan HTTP GET ke endpoint API (misalnya `/api/education/`).
  - Fungsi *view* menerima permintaan tersebut dan mengambil data dari database SQLite menggunakan QuerySet Django ORM (`Education.objects.all()`).
  - QuerySet yang berisi objek-objek Python tersebut diserahkan ke *serializer* (`serializers.serialize("json", education_list)`) untuk diubah menjadi rentetan string berformat JSON.
  - Fungsi *view* merangkum string JSON tersebut ke dalam objek `HttpResponse` dengan header `content_type="application/json"` dan mengirimkannya kembali ke *client*.
     **Mengapa Perlu Serialization?**:
  Model Django atau QuerySet berupa objek Python kompleks yang tersimpan di dalam memori server dan tidak bisa ditransmisikan secara langsung melalui protokol HTTP. *Serialization* bertugas memutus (*convert*) struktur objek kompleks tersebut menjadi format teks standar (seperti string JSON/XML) agar dapat dikirim melalui jaringan dan dipahami oleh aplikasi *client* dalam bahasa pemrogramman apa pun.


### Tugas 4

## AI Disclosure

- **Tools Digunakan**: Gemini AI
- **Tujuan**: Membantu penyelesaian bug `ImportError`, perancangan otorisasi 4 peran (Pengunjung, Pengguna Biasa, Editor, Superuser), pembuatan komponen `project_star.html`, serta pengisian variabel cookie `last_login`.
- **Perbaikan Manual**:
  1. Menghapus fungsi duplikat (*duplicate functions*) pada `main/views.py`.
  2. Menyesuaikan logika `is_editor_or_superuser` dengan helper group check `request.user.groups.filter(name='Editor').exists()`.
  3. Mengatur struktur visibilitas tombol aksi pada template `templates/education.html` dan `templates/index.html`.
