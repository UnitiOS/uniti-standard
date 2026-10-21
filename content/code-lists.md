# Daftar kode

Status: draf

## 1. Tujuan

Daftar kode yang sudah baku dipakai langsung, tidak dibuat ulang
([`00-prinsip`](../00-prinsip.md) P8). Dokumen ini menyebut daftar kode luar
yang dipakai standar, kode mana yang dipakai, dan alamatnya, supaya kode itu
bisa menjadi nilai pilihan seperti pilihan lain
([`03-nilai`](../bentuk/03-nilai.md) §2.3 dan §2.6).

## 2. Daftar kode luar yang dipakai

| Daftar | Standar luar | Dipakai untuk | Alamat |
|---|---|---|---|
| Mata uang | ISO 4217 | Satuan uang | `uniti/satuan/Satuan` |
| Satuan lain | UCUM (*Unified Code for Units of Measure*) | Satuan massa, panjang, dan lama waktu | `uniti/satuan/Satuan` |
| Bahasa | BCP 47 | Kode bahasa di label dan teks | belum diberi alamat |

Mata uang dan satuan lain ada di satu daftar, karena `satuan(n)` memberi
satuan sebuah angka sebagai pilihan dari satu daftar
([`06-aturan-hitung`](../bentuk/06-aturan-hitung.md) §2.5).

Kode bahasa hanya dipakai di cara menulis label dan teks. Belum ada kasus yang
mencatat bahasa sebagai nilai, jadi daftarnya belum diberi alamat.

## 3. Daftar satuan

```uniti
module uniti/unit@v1

choice_list Unit, code
  label.en       Unit
  label.id       Satuan
  definition.en  Unit of measure, including currencies. Every number with a
                 unit uses a unit from this list.
  note.en        Currency codes come from ISO 4217 and other unit codes from
                 UCUM, except calendar months and years.
  choices:
    IDR
    USD
    s
    min
    h
    d
    wk
    month
    year
    g
    kg
    mm
    cm
    m
    km
```

Arti setiap kode, dan cara menulisnya di notasi acuan:

| Kode | Besaran | Ditulis di notasi acuan | Hubungan tetap | Asal kode |
|---|---|---|---|---|
| `IDR` | money | `IDR` | — | ISO 4217 |
| `USD` | money | `USD` | — | ISO 4217 |
| `s` | duration | `second` | satuan dasar | UCUM |
| `min` | duration | `minute` | 1 min = 60 s | UCUM |
| `h` | duration | `hour` | 1 h = 60 min | UCUM |
| `d` | duration | `day` | 1 d = 24 h | UCUM |
| `wk` | duration | `week` | 1 wk = 7 d | UCUM |
| `month` | duration | `month` | satuan dasar kalender | Uniti |
| `year` | duration | `year` | 1 tahun = 12 bulan | Uniti |
| `g` | mass | `g` | satuan dasar | UCUM |
| `kg` | mass | `kg` | 1 kg = 1.000 g | UCUM |
| `mm` | length | `mm` | 1.000 mm = 1 m | UCUM |
| `cm` | length | `cm` | 100 cm = 1 m | UCUM |
| `m` | length | `m` | satuan dasar | UCUM |
| `km` | length | `km` | 1 km = 1.000 m | UCUM |

Satuan hanya bisa diubah ke satuan lain yang hubungannya tetap
(06 §2.5, `ubah`). Uang tidak punya hubungan tetap, karena kurs dicatat sebagai
fakta. Bulan dan tahun juga tidak punya hubungan tetap dengan hari, karena
panjang bulan berbeda-beda.

**Bulan dan tahun kalender** adalah kode milik Uniti. Kode UCUM `mo` dan `a`
artinya panjang rata-rata, 30,4375 hari dan 365,25 hari, dan tidak sama
dengan satu bulan atau satu tahun kalender. UCUM tidak punya kode untuk bulan
kalender.

## 4. Besaran

| Besaran | Satuan |
|---|---|
| `money` | Kode mata uang |
| `duration` | `s`, `min`, `h`, `d`, `wk`, `month`, `year` |
| `mass` | `g`, `kg` |
| `length` | `mm`, `cm`, `m`, `km` |

Besaran turunan ditulis dengan cara yang sama seperti satuannya, misalnya
`panjang²` untuk luas dan `uang/lama_waktu` untuk tarif (lampiran A §2.4).

## 5. Menambah kode

Daftar ini isi. Kode baru ditambahkan lewat versi baru `uniti/satuan`, tanpa
mengubah bentuk:
- kode dari standar luar ditulis persis seperti di standar luarnya;
- kode milik Uniti hanya dibuat bila standar luarnya tidak punya padanan,
  seperti bulan dan tahun kalender;
- kode dipilih karena dibutuhkan, bukan karena ada di standar luar.
