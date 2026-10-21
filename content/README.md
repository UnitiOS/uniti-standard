# Isi

Status: draf; tahap 6 selesai
Dibuka: 2026-10-20

Bagian B standar: isi yang dipakai bersama. Bentuknya mengikuti bagian A,
dan isinya boleh terus bertambah tanpa mengubah bentuk
([`keputusan/0002`](../keputusan/0002-bentuk-tetap-isi-bebas.md)).

## 1. Tujuan tahap 6

Tahap 6 ([`keputusan/0004`](../keputusan/0004-cara-menulis.md)) menulis isi
awal: templat kartu, daftar kode, pustaka hitung, dan kamus pertama. Isi awal
ini juga menguji satu hal yang belum pernah diuji, yaitu modul dalam **bentuk
lengkap**, yang akan dibekukan di tahap 7.

Cakupannya sengaja sempit. Kamus pertama hanya memuat isi yang sudah
dibutuhkan kasus dari minimal dua domain. Isi lain menunggu sesudah v0.1, dan
masuk lewat aturan masuk kamus (§3).

## 2. Peta isi

| No | Berkas | Isinya | Modul |
|---|---|---|---|
| B1 | `isi/README.md` | Berkas ini: peta isi dan aturan masuk kamus | — |
| B2 | [`templat-kartu.md`](templat-kartu.md) | Templat kartu konsep, kartu sifat, daftar pilihan, sifat hitungan, syarat, dan bantu, dalam notasi acuan | — |
| B3 | [`daftar-kode.md`](daftar-kode.md) | Daftar kode luar yang dipakai: mata uang (ISO 4217), satuan (UCUM, hanya yang dipakai), dan bahasa (BCP 47), ditambah daftar besaran | `uniti/satuan@v1` |
| B4 | [`hitung.md`](hitung.md) | Pustaka hitung, dipindah dari `uji/acuan/pustaka/hitung.md` dan ditulis dalam bentuk lengkap. Aturannya tidak berubah | `uniti/hitung@v1` |
| B5 | [`kamus/`](kamus/) | Kamus pertama: tiga modul di §4 | `uniti/pihak@v1`, `uniti/barang@v1`, `uniti/pembayaran@v1` |
| B6 | Uji | Penghitung acuan memeriksa bentuk lengkap, membaca daftar kode, dan menjalankan kasus [`17-kamus.md`](../uji/acuan/kasus/17-kamus.md) | — |

Semua modul isi dibekukan sebagai v1 saat v0.1 dikunci (tahap 8).

## 3. Aturan masuk kamus

Syaratnya sudah ada di bagian A. Tahap 6 hanya mengumpulkannya di satu
tempat, ditambah satu syarat dari gerbang temuan
([`keputusan/0046`](../keputusan/0046-gerbang-temuan.md)):

1. **Dibutuhkan, bukan dibayangkan.** Konsep atau sifat masuk kamus hanya
   bila sudah dibutuhkan modul dari minimal dua domain yang berbeda.
2. **Kartu lengkap.** Yang termasuk dan yang tidak termasuk diambil dari
   minimal dua domain (KONSEP-2).
3. **Contoh dari dua domain** untuk setiap sifat hitungan, sumbangan, dan
   syarat (BUKTI-16).
4. **Jembatan** ke standar luar bila padanannya ada (HUBUNGAN-11).

Siapa yang memutuskan sebuah usulan masuk kamus termasuk tata kelola, dan
ditunda ke v0.2 bersama `09-kepemilikan`
([`keputusan/0048`](../keputusan/0048-kepemilikan-ke-v02.md)).

## 4. Kamus pertama

Hanya isi yang lolos syarat 1 menurut kasus yang sudah ada di
[`uji/acuan/kasus/`](../uji/acuan/kasus/):

| Modul | Isi | Kasus yang membutuhkannya |
|---|---|---|
| [`uniti/pihak`](kamus/pihak.md) | Pihak, Orang, Organisasi | organisasi (o2), keuangan (k2), klinik (c2), dan peran di penggajian, langganan, sekolah, dan loyalitas, misalnya karyawan, pelanggan, dan siswa |
| [`uniti/barang`](kamus/barang.md) | Barang, sifat `barang` | persediaan (p1 sampai p4), penyewaan (s1, s4), manufaktur (m1) |
| [`uniti/pembayaran`](kamus/pembayaran.md) | Pembayaran, sifat `jumlah`, `tanggal`, dan `cara_bayar`, daftar CaraBayar | pinjaman (j2, j3), klinik dan apotek (16), faktur (13) |

Sifat untuk ketiga konsep itu masuk kamus hanya bila sifat yang sama dipakai
kasus dari dua domain. Sifat lainnya tetap di modul pemakainya, lewat
"berlaku untuk" (04 §2.3). Karena itu Pihak belum punya sifat apa pun: belum
ada kasus yang mencatat nama atau sifat lain sebuah pihak.

Yang **tidak** masuk kamus pertama:
- `uniti/umum` dengan sifat `nama` dan `catatan`: disebut sebagai contoh di
  04 dan 05, tetapi belum ada kasus yang membutuhkannya;
- `Transaksi`: disebut sebagai contoh induk di 04, tetapi belum ada kasus;
- `Kelas` dan daftar alasan tidak hadir: disebut sebagai contoh kamus di 03,
  04, dan 05, tetapi baru dibutuhkan satu domain.

## 5. Celah

I1 sampai I3 sudah terlihat sebelum isi ditulis. I4 sampai I7 ditemukan saat
menulisnya.

| No | Celah | Golongan menurut 0046 | Usulan |
|---|---|---|---|
| I1 | Kode dari standar luar memakai huruf besar dan tanda yang tidak boleh ada di nama pilihan (ALAMAT-2), misalnya `IDR`, `Cel`, dan `[in_i]`. UCUM juga membedakan huruf besar dan kecil, jadi kodenya tidak bisa diubah menjadi huruf kecil. Akibatnya pilihan dari daftar kode tidak bisa diberi alamat (A29) | **Lolos.** Muncul dari kasus K2 (kurs), dan mesin tidak bisa memutuskan apakah alamat seperti itu sah | Pilihan dari daftar kode memakai kode aslinya, persis. Alamatnya alamat modul, lalu kodenya: `uniti/satuan/IDR`. Ditambah satu kata di baris kepala: `daftar Satuan, kode`. Diputuskan di [`keputusan/0050`](../keputusan/0050-daftar-kode.md) |
| I2 | Lampiran A §2.4 menyebut UCUM `mo` dan `a` sebagai padanan `bulan` dan `tahun`. Padahal di UCUM keduanya panjang rata-rata, yaitu 30,4375 hari dan 365,25 hari, sedangkan bulan dan tahun Uniti adalah bulan dan tahun kalender | Isi: daftar kode | `bulan` dan `tahun` menjadi kode milik Uniti di daftar kode, dengan catatan tentang UCUM |
| I3 | Dokumen bentuk memakai alamat kamus yang tidak seragam: `uniti/barang/Barang` dan `uniti/persediaan/Barang`, `uniti/barang/nama` dan `uniti/umum/nama` | Perbaikan contoh | Disamakan dengan kamus pertama |
| I4 | Versi daftar kode yang berlaku bagi modul yang menulis satuan tanpa memakai `uniti/satuan` | Ditunda | Contoh hanya memakai kode di versi pertama |
| I5 | Bagian wajib kartu daftar pilihan tidak disebut, sehingga dua implementasi bisa berbeda tentang boleh tidaknya sebuah modul dibekukan | **Lolos.** Muncul saat menulis `CaraBayar`, `CaraBulat`, dan `CaraSisa` | Label dan arti wajib, seperti kartu sifat (NILAI-19) |
| I6 | Jembatan untuk daftar pilihan tidak punya cara tulis | Ditunda: HUBUNGAN-11 hanya anjuran | — |
| I7 | Arah jumlah pembayaran berbeda antarkasus: `berkurang` di pinjaman, `bertambah` di klinik | Isi | Di kamus jumlahnya tanpa arah |

Daftar kode luar dipakai langsung, tidak dibuat ulang (P8). Uniti hanya
memilih kode yang dipakai dan menyebut cara menulisnya di notasi acuan,
misalnya `hari` untuk UCUM `d`. Faktor antarsatuan diambil dari UCUM.
Kalau daftarnya bertambah, yang berubah adalah isi, bukan bentuk.

## 6. Yang tidak dikerjakan di tahap 6

- Daftar negara, dan zona waktu menurut wilayah (IANA). Belum ada kasus yang
  membutuhkannya. Zona waktu tetap ditulis sebagai selisih dari UTC di
  lampiran A.
- Proses dan pemutus usulan kamus: v0.2.
- Terjemahan bahasa Inggris: sesudah v0.1 stabil.
- Konsep kamus selain yang ada di §4.

## 7. Kriteria selesai

1. B1 sampai B5 tertulis. Setiap modul kamus dan pustaka lolos pemeriksaan
   kartu bentuk lengkap oleh penghitung acuan.
2. Setiap kartu konsep kamus memuat yang termasuk dan yang tidak termasuk
   dari dua domain. Ini diperiksa dengan membaca, karena mesin tidak tahu
   domain sebuah kalimat.
3. Satu kasus dengan dua domain yang memakai kamus pertama lulus, dan semua
   contoh lama tetap lulus.
4. A29 selesai, dan lampiran A §2.4 tidak lagi bertanda [sementara].
5. Setiap temuan sudah digolongkan menurut 0046.

## 8. Hasil

Kelima kriteria terpenuhi.

1. Keempat modul `uniti/*` di isi lolos pemeriksaan bentuk lengkap
   (`program/lengkap.py`). Pustaka hitung ditulis ulang dalam bentuk lengkap
   karena TULIS-17. Aturannya tidak berubah, dan 6.400 perbandingan acak
   dengan operasi lama masih sama.
2. Setiap kartu konsep kamus memuat yang termasuk dan yang tidak termasuk
   dari dua domain. Domainnya ditulis di awal kalimat, dan uji kecil
   memeriksa bahwa awalannya berbeda.
3. Kasus [`17-kamus.md`](../uji/acuan/kasus/17-kamus.md) lulus: toko
   penyewaan dan sekolah memakai kamus yang sama. Kasus 16 kini memakai kamus
   pembayaran yang sebenarnya. Seluruhnya 139 contoh dan 172 uji lulus.
4. A29 selesai. K2 kembali seperti uji kertas, dengan mata uang asal dan
   tujuan kurs sebagai pilihan. Lampiran A §2.4 tidak lagi bertanda
   [sementara].
5. Temuannya ada di §5. Dua lolos gerbang: I1 diputuskan di
   [`keputusan/0050`](../keputusan/0050-daftar-kode.md), dan I5 di
   [`keputusan/0051`](../keputusan/0051-pelengkap-dari-isi-awal.md). Sisanya
   isi, perbaikan contoh, atau ditunda.

Penghitung acuan juga kini memeriksa dua aturan yang sudah ada sebelumnya:
NILAI-13, pilihan dari modul lain hanya masuk ke daftar terbuka, dan
KONSEP-8, sifat milik pihak lain tidak boleh dinyatakan wajib.
