# Templat kartu

Status: draf

Templat untuk menulis kartu dalam bentuk lengkap, yaitu bentuk untuk modul
yang akan dibekukan (lampiran A §2.8, TULIS-17). Bagian yang wajib menurut
standar diberi tanda *wajib*. Bagian lain boleh ditulis atau ditinggalkan.

Tulisan di antara `‹ ›` diganti dengan isinya. Contoh yang sudah terisi ada di
[`kamus/`](kamus/).

Penghitung acuan memeriksa bagian yang wajib dengan
`python -m program.lengkap ‹berkas›`, dari folder `uji/acuan`.

## Kartu konsep

```
concept ‹ConceptName›
  label.en       ‹name for humans›                       # required, CONCEPT-1
  definition.en  ‹what this concept is, one or two sentences›   # required, CONCEPT-1
  parent         ‹ParentConcept›                         # at most one
  includes.en    ‹Domain›: ‹things that belong›          # required, at least one
  excludes.en    ‹Domain›: ‹things that look similar but do not belong, and
                 why›                                    # required, at least one
  similar        ‹full address or IRI›                   # bridge, optional
  note.en        ‹extra remarks›
```

Di kamus, yang termasuk dan yang tidak termasuk masing-masing diambil dari
minimal dua domain (KONSEP-2). Domainnya ditulis di awal kalimat, misalnya
"Klinik: …", supaya mudah diperiksa saat membaca.

## Kartu sifat

```
property ‹property_name› : ‹value type›                  # required, CONCEPT-3
  label.en       ‹name for humans›                       # required
  definition.en  ‹what this property states›             # required
  personal       ‹yes or no›                             # required [provisional]
  same_as        ‹full address or IRI›                   # bridge, optional
  note.en        ‹extra remarks›
```

Jenis nilai ditulis di baris kepala: `teks`, `angka (‹besaran›, ‹arah›)`,
`ya_tidak`, `tanggal`, `saat`, `pilihan ‹Daftar›`, atau `rujukan ‹Konsep›`,
ditambah `, banyak` untuk sifat yang banyak nilainya (lampiran A §2.8).

## Kartu daftar pilihan

```
choice_list ‹ListName›, ‹open, closed, or code›
  label.en       ‹name for humans›                       # required, VALUE-19
  definition.en  ‹which choices this list holds›         # required, VALUE-19
  choices:
    ‹first_choice›
    ‹second_choice›
```

## Sifat hitungan

```
computed ‹Concept›.‹name›(‹parameters›) : ‹value type›, ‹open or closed›
  label.en       ‹name for humans›                       # required, CALC-4
  definition.en  ‹what is computed›                      # required
  personal       ‹yes or no›                             # required [provisional]
  rule:
    ‹expression›
```

## Syarat

```
constraint ‹Concept›.‹name›
  label.en       ‹name for humans›                       # required, CALC-37
  definition.en  ‹what is guarded›                       # required
  message.en     ‹sentence for humans when rejected›     # required
  rule:
    ‹yes/no expression›
```

## Bantu

```
helper ‹name›(‹parameters›) : ‹result type›
  definition.en  ‹what is produced›
  rule:
    ‹expression›
```

Bantu tidak punya bagian kartu yang wajib, tetapi tetap ditulis dalam bentuk
lengkap di modul yang akan dibekukan.
