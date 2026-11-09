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

1. **Apa perbedaan antara autentikasi dan otorisasi dalam konteks aplikasi web? Jelaskan bagaimana Django memfasilitasi kedua konsep tersebut.**  
   * **Autentikasi (*Authentication*)**: Proses untuk membuktikan dan memverifikasi identitas pengguna (menjawab pertanyaan *"Siapakah Anda?"*). Dalam Django, proses ini ditangani oleh sistem autentikasi bawaan menggunakan model `User`, fungsi `authenticate()`, serta fungsi `login()` dan `logout()` yang mengelola sesi login berbasis cookie.  
   * **Otorisasi (*Authorization*)**: Proses untuk menentukan hak akses yang dimiliki oleh pengguna yang telah terautentikasi (menjawab pertanyaan *"Apa yang boleh Anda lakukan?"*). Dalam Django, hal ini difasilitasi melalui atribut `is_superuser`, atribut `is_staff`, sistem `Groups`, serta dekorator/pengecekan izin seperti `@permission_required` atau pengecekan kepemilikan data di fungsi view.

2. **Jelaskan peran grup dalam sistem autentikasi dan otorisasi Django.**  
   Grup (`django.contrib.auth.models.Group`) berfungsi sebagai pengelompokan pengguna yang memiliki tanggung jawab atau hak akses serupa (*Role-Based Access Control*). Dengan grup, administrator tidak perlu memberikan izin (*permissions*) secara satu per satu ke setiap akun pengguna. Saat izin diberikan ke suatu grup (misalnya grup `Editor`), semua anggota grup tersebut secara otomatis mewarisi hak akses yang sama. Hal ini mempermudah manajemen peran dalam aplikasi portofolio, seperti membedakan pengguna biasa dengan Editor.

3. **Mengapa penggunaan cookie perlu dibatasi atau dikelola dengan bijak pada aplikasi web? Jelaskan risiko keamanan yang mungkin terjadi jika cookie tidak dikelola dengan benar.**  
   Cookie disimpan langsung di browser pengguna (*client-side*), sehingga memiliki risiko keamanan jika tidak dikonfigurasi dengan ketat:  
   * **Pencurian Sesi (*Session Hijacking via XSS*)**: Jika cookie sesi tidak dilindungi flag `HttpOnly`, skrip berbahaya yang disuntikkan penyerang dapat membaca nilai cookie sesi via JavaScript (`document.cookie`) dan menyamar sebagai pengguna yang sah.  
   * **Serangan CSRF (*Cross-Site Request Forgery*)**: Cookie otomatis dikirimkan oleh browser pada setiap request ke domain asal. Jika cookie tidak dikonfigurasi dengan atribut `SameSite` yang tepat atau tidak dilengkapi token CSRF, situs berbahaya dapat memicu aksi yang tidak diinginkan atas nama pengguna.  
   * **Kebocoran Jaringan (*Man-In-The-Middle*)**: Cookie yang tidak menggunakan atribut `Secure` dapat ditransmisikan melalui protokol HTTP yang tidak terenkripsi sehingga rentan disadap.

### Tugas 5

1. **Jelaskan mengapa kita menggunakan AJAX untuk mengambil dan mengirim data daripada me-refresh seluruh halaman.**  
   AJAX (*Asynchronous JavaScript and XML*) memungkinkan pertukaran data antara browser dan server terjadi di latar belakang (*asynchronous*) tanpa perlu memuat ulang (*full reload*) seluruh halaman web. Keuntungannya:
   * **Pengalaman Pengguna (UX) yang Lebih Halus**: Halaman tidak berkedip (*no flicker*) saat pengguna mencari, menambah, atau memfilter data.
   * **Hemat Bandwidth & Lebih Cepat**: Hanya payload data murni (JSON) yang dikirim melalui jaringan, bukan seluruh dokumen HTML, stylesheet, dan skrip yang berulang.

2. **Fungsi `await` pada `fetch()` dan dampaknya jika tidak menggunakannya:**  
   Fungsi `await` digunakan untuk menghentikan sementara eksekusi fungsi `async` sampai objek `Promise` yang dikembalikan oleh `fetch()` selesai (*resolved* atau *rejected*).  
   * **Jika tidak menggunakan `await`**: Variabel penampung hasil `fetch()` tidak berisi respon HTTP nyata, melainkan objek `Promise` dalam status *pending*. Hal ini menyebabkan kode berikutnya (seperti `.json()`) gagal dieksekusi atau menghasilkan error *undefined* karena JavaScript langsung mengeksekusi baris berikutnya tanpa menunggu data selesai diunduh dari server.

3. **Apa itu serangan XSS (Cross-Site Scripting) dan mengapa rendering AJAX/JavaScript lebih rentan dibandingkan Django Template?**  
   **Cross-Site Scripting (XSS)** adalah jenis serangan di mana penyerang menyisipkan skrip JavaScript berbahaya ke dalam aplikasi web yang kemudian dieksekusi oleh browser pengguna lain.  
   * **Mengapa AJAX/JavaScript lebih rentan?** Secara bawaan, Django Template Engine memiliki fitur **auto-escaping** otomatis yang mengubah karakter khusus HTML (seperti `<` dan `>`) menjadi entitas aman (`&lt;` dan `&gt;`). Namun, saat kita menggunakan AJAX dan me-render data ke elemen HTML menggunakan properti JavaScript seperti `innerHTML`, fitur perlindungan Django hilang. Browser akan menafsirkan data string tersebut langsung sebagai struktur HTML/skrip JavaScript aktif, sehingga membuka celah Stored XSS jika data dari server mengandung skrip berbahaya. Oleh karena itu, kita wajib melakukan sanitasi manual di sisi client menggunakan fungsi `escapeHtml()` atau `textContent`.

### Tugas 6

#### 1. REST & HTTP Methods
* **Konsep REST dan Batasan JSON**: REST (*Representational State Transfer*) adalah gaya arsitektur antarmuka perangkat lunak berbasis sumber daya (*resource-based*), *stateless*, dan memanfaatkan metode protokol HTTP standar secara konsisten. Sekadar mengembalikan format JSON **belum cukup** untuk mengkategorikan sebuah API sebagai RESTful karena:
  1. **Berorientasi Resource (Bukan Aksi/RPC)**: Endpoint RESTful harus menggunakan kata benda jamak untuk mengidentifikasi entitas (misalnya `/api/v1/education/` dan `/api/v1/education/<id>/`), bukan kata kerja prosedural seperti `/api/get_education/` atau `/api/delete_education_by_id/`.
  2. **Penggunaan HTTP Verbs yang Tepat**: Operasi CRUD wajib dipetakan ke metode HTTP semantik (GET untuk membaca, POST untuk membuat, PUT/PATCH untuk memperbarui, DELETE untuk menghapus), bukan merutekan seluruh manipulasi data melalui POST atau GET saja.
  3. **Pemanfaatan HTTP Status Code Semantik**: Respon wajib mencerminkan status sebenarnya menggunakan kode status HTTP standar (misal 201 Created, 204 No Content, 400 Bad Request, 403 Forbidden, 404 Not Found), bukan mengembalikan 200 OK dengan isi JSON bertuliskan `{"status": "error"}`.
  4. **Prinsip Stateless**: Setiap permintaan dari klien harus memuat seluruh konteks yang diperlukan tanpa bergantung pada status tersimpan di server secara tersembunyi.
* **Perbedaan PUT dan PATCH beserta Contoh Penggunaannya**:
  * **PUT**: Digunakan untuk pembaruan sumber daya secara menyeluruh (*full update / idempotent*). Klien mengirimkan representasi lengkap dari entitas; atribut yang tidak disertakan akan direset ke nilai default atau menjadi kosong.  
    *Contoh*: Ketika pengguna mengedit seluruh formulir data pendidikan melalui modal edit lengkap (mengirimkan kembali seluruh field `institution`, `degree`, `description`, `started_year`, dan `ended_year`).
  * **PATCH**: Digunakan untuk pembaruan sebagian atribut saja (*partial update / non-idempotent*). Klien hanya mengirimkan atribut yang ingin diubah, sementara atribut lain dipertahankan tanpa perubahan.  
    *Contoh*: Ketika pengguna hanya ingin memperbarui status tahun kelulusan `ended_year: 2026` saat baru saja wisuda, tanpa perlu mengirim ulang deskripsi atau tahun mulai.

#### 2. Peran Serializer pada Django REST Framework (DRF)
* **Peran Serializer**:
  1. **Serialization**: Mengonversi objek kompleks Django (seperti QuerySet atau model instance `Education`) menjadi struktur data bawaan Python (dictionary/list) yang dapat dengan mudah dirender ke format JSON.
  2. **Deserialization & Validasi**: Memvalidasi data JSON masuk dari klien terhadap aturan tipe data dan batasan model, membersihkan nilai (*sanitization*), serta mengubahnya kembali menjadi objek Python/database melalui method `.is_valid()` dan `.save()`.
* **Keuntungan Dibanding Merakit Dictionary Manual (`JsonResponse`)**:
  * **Validasi Otomatis & Terstruktur**: Serializer menyediakan validasi deklaratif di tingkat field (`validate_<field>`) dan pembersihan otomatis (misalnya `strip_tags` untuk sanitasi XSS), serta otomatis mengembalikan struktur error 400 Bad Request jika data tidak valid.
  * **Mendukung Alur Baca-Tulis Dua Arah**: Merakit manual dengan `JsonResponse` hanya menangani pembacaan (output satu arah), sedangkan Serializer menangani pembacaan sekaligus penulisan, validasi, dan persistensi database secara terpadu.
  * **Keamanan & Kontrol Field**: Menghindari kerentanan *mass assignment* dan kebocoran data sensitif (misalnya password hash atau data privat) karena field yang terekspos dan yang dapat ditulis didefinisikan secara eksplisit via `fields` dan `read_only_fields`.
  * **Field Terhitung Dinamis**: Mempermudah penyertaan field kalkulasi seperti `star_count`, `is_starred`, dan `starred_by_names` via `SerializerMethodField`.

#### 3. Autentikasi vs Otorisasi & Pemeriksaan di Server
* **Perbedaan Autentikasi dan Otorisasi**:
  * **Autentikasi (*Authentication*)**: Proses verifikasi keaslian identitas pengguna untuk menjawab pertanyaan *"Siapakah Anda?"* (misalnya mengonfirmasi identitas pengguna lewat cookie sesi pada `SessionAuthentication`).
  * **Otorisasi (*Authorization / Permission*)**: Proses verifikasi hak akses pengguna untuk menjawab pertanyaan *"Boleh melakukan apa Anda?"* (misalnya memastikan apakah pengguna memiliki hak sebagai Editor untuk mengubah data, atau sebagai Superuser untuk menghapus data).
* **Mengapa Hak Akses Harus Diperiksa dengan Permission Class di Server**:
  * Menyembunyikan tombol aksi pada template HTML hanya memengaruhi kenyamanan visual di antarmuka (*client-side UI sugar*).
  * Klien berada di luar kendali server. Siapa pun dapat menembakkan permintaan HTTP secara langsung menggunakan cURL, Postman, atau Fetch API melalui Console DevTools browser.
  * Jika server tidak menegakkan validasi hak akses melalui `permission_classes` (seperti `IsPortfolioOwnerOrEditorOrReadOnly`), penyerang atau pengguna tanpa izin dapat memanggil endpoint `DELETE /api/v1/education/<id>/` secara langsung dan menghapus data database. Server adalah garis pertahanan terakhir dan mutlak.

#### 4. Kebutuhan Token CSRF & Keterbatasan `force_authenticate`
* **Mengapa Permintaan Mutasi Tetap Memerlukan Token CSRF pada `SessionAuthentication`**:
  * `SessionAuthentication` memanfaatkan cookie sesi browser (`sessionid`) untuk memverifikasi identitas pengguna yang sedang login. Browser secara otomatis menyertakan cookie ini pada setiap permintaan HTTP yang dikirimkan ke domain aplikasi, termasuk permintaan lintas situs yang dipicu secara licik oleh website berbahaya (*Cross-Site Request Forgery*).
  * Tanpa perlindungan token CSRF, penyerang dapat memanipulasi browser korban yang sedang membuka tab lain untuk mengirim permintaan `DELETE` atau `POST` ke API portofolio. Header `X-CSRFToken` membuktikan bahwa request tersebut memang diprakarsai oleh aplikasi klien resmi kita, bukan dari situs pihak ketiga.
* **Mengapa `force_authenticate` Tidak Cukup untuk Membuktikan Perlindungan CSRF**:
  * Fungsi `force_authenticate()` pada DRF bekerja dengan menyuntikkan objek `request.user` secara langsung dan sintetis ke dalam request pengujian, sehingga secara sengaja **melewati (*bypass*)** seluruh alur middleware autentikasi dan pengecekan CSRF bawaan Django.
  * Oleh karena itu, pengujian yang hanya memakai `force_authenticate()` tidak pernah benar-benar menguji apakah middleware CSRF bekerja menolak permintaan tanpa token. Pengujian CSRF yang sahih wajib menggunakan `APIClient(enforce_csrf_checks=True)` dan fungsi autentikasi nyata (`.login()`) untuk membuktikan penolakan 403 Forbidden saat token tidak disertakan.

---

### AI Disclosure

* **Alat AI yang Digunakan**: Google Antigravity Assistant (ditenagai model Gemini 3.8 Flash).
* **Strategi Prompting**:
  1. *Audit & Verification Prompting*: Meminta asisten untuk meninjau secara mendalam repositori terhadap seluruh kriteria checklist tugas (Model, Migration, Serializer, Permissions, API Views, URLs, Frontend Integration, Unit Testing, dan CSRF enforcement).
  2. *Step-by-Step Task Execution*: Menjalankan eksekusi terstruktur mulai dari penambahan relasi star model `Education` dan migrasinya, penulisan serializer dan view DRF dengan SessionAuthentication, pembuatan endpoint star, integrasi penuh modal Edit/Tambah/Hapus/Star di template frontend, hingga penulisan suite test komprehensif `EducationAPITest`.
* **Bagian yang Dibantu AI**:
  * Mengidentifikasi akar masalah error runtime (`NameError: name 'Education' is not defined` dan inkonsistensi tipe UUID pada Project).
  * Menyusun class `EducationSerializer` dengan validasi teks `strip_tags` dan field kalkulasi star `SerializerMethodField`.
  * Membangun fungsi view REST API `education_list`, `education_detail`, dan `education_star` di `main/api_views.py`.
  * Memodernisasi template `templates/education.html` ke arsitektur RESTful DRF lengkap dengan modal Edit AJAX (PATCH/PUT) dan penanganan toast error.
  * Menuliskan pengujian otomatis `EducationAPITest` (27 unit test) mencakup skenario 4 peran, verifikasi mutasi database, dan penolakan CSRF menggunakan `APIClient(enforce_csrf_checks=True)`.
* **Analisis Kritis & Koreksi Manual**:
  * Awalnya terdapat inkonsistensi tipe primary key antara model `Project` dan konverter URL `<uuid:...>`. Model `Project` diperbaiki agar memiliki UUID eksplisit dan dilakukan migrasi database baru (`0006_education_starred_by_alter_project_id`), memastikan kompatibilitas penuh dengan pengujian Tutorial 07.
  * Pengujian CSRF diuji secara eksplisit menggunakan `.login()` sungguhan guna memastikan perlindungan keamanan di sisi server benar-benar aktif menolak request mutasi tanpa token.
