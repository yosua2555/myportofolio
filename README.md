Nama : Yosua Peitho Purba
NPM : 2506657402
Kelas : PBP D

### Tugas 1

1. Penggunaan Elemen Semantik HTML5
Ya, saya menggunakan elemen semantik HTML5 seperti <header>, <main>, <section>, dan <footer> dalam merancang struktur kode HTML dalam portofolio ini. Elemen-elemen ini sangat membantu dalam membuat *static web* karena membuat struktur kode menjadi jauh lebih bersih, terorganisir, dan mudah dibaca (*readable*). Selain itu, penggunaan elemen semantik memberikan konteks yang jelas bagi mesin pencari (*SEO*) dan pembaca layar (*accessibility*), sehingga bagian identitas utama, bagian pengalaman (*experience*), hingga bagian keahlian (*skills*) terisolasi dengan logis di dalam dokumen.

2. Tantangan utama dalam menjaga portofolio tetap responsif adalah mengatur proporsi tata letak elemen *Hero* yang memiliki grid yang tidak simetris antara teks identitas, detail informasi, dan foto profil, agar tidak berantakan saat beralih ke layar kecil (*mobile*). Untuk mengevaluasinya, saya memprioritaskan keterbacaan konten utama dan konsistensi hierarki visual terlebih dahulu. Ketika beralih dari *desktop* ke *mobile*, saya menggunakan *media queries* dengan mengubah struktur *grid-template-areas* serta mengatur ulang lebar elemen menggunakan unit relatif dan *flex-direction: column*, sehingga foto profil dan informasi teks dapat tersusun secara vertikal dengan rapi tanpa terpotong.

3. Sebagai *static web* murni, batasannya terletak pada interaktivitas yang terbatas; informasi bersifat kaku (*hardcoded*), tidak ada penyimpanan basis data (*database*), dan tidak ada fitur umpan balik langsung seperti formulir kontak yang dapat memproses pesan secara *real-time*. Berdasarkan batasan tersebut, fungsionalitas dinamis yang ingin saya tambahkan pada iterasi proyek selanjutnya adalah sistem manajemen konten (CMS) berbasis Django untuk mengelola daftar proyek atau *experience* secara dinamis melalui halaman *admin*, serta integrasi *contact form* interaktif yang dilengkapi validasi sisi server dan sistem pengiriman email otomatis.