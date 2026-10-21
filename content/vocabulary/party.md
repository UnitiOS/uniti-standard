# Pihak

Status: draf

Siapa yang bertindak, memiliki, atau berjanji: orang dan organisasi. Peran
seperti pelanggan, karyawan, dan siswa bukan konsep di sini. Peran dicatat
sebagai rujukan dari hal lain ke sebuah pihak
([`04-konsep`](../../bentuk/04-konsep.md) §2.5, KONSEP-13).

Kamus ini belum memuat sifat apa pun. Belum ada sifat pihak yang dipakai
kasus dari dua domain, termasuk nama ([`isi/README.md`](../README.md) §3).

```uniti
module uniti/party@v1

concept Party
  label.en       Party
  label.id       Pihak
  definition.en  A person or organization that can act, own something, or
                 make a promise to another party.
  includes.en    Rental: Budi, who rents a tent.
  includes.en    Clinic: Klinik Sehat, which receives payments from
                 patients.
  excludes.en    Shop: "customer". That is the role of a party in a sale,
                 recorded as a reference from the sale to its party.
  excludes.en    Organization: the position "manager". That is a person's
                 standing within an employment contract, not a party.
  similar        http://xmlns.com/foaf/0.1/Agent

concept Person
  label.en       Person
  label.id       Orang
  definition.en  A human being.
  parent         Party
  includes.en    Organization: an employee bound by an employment contract.
  includes.en    School: a student who attends a class.
  excludes.en    Rental: Toko Kemah Ceria, even though one person owns it.
                 The shop is an organization.
  excludes.en    Loyalty: a member account in a points program. One person
                 can have more than one account.
  similar        https://schema.org/Person

concept Organization
  label.en       Organization
  label.id       Organisasi
  definition.en  A group of people who act together as one party, for
                 example a business, an institution, or an association.
  parent         Party
  includes.en    Finance: a company that records its revenue.
  includes.en    Clinic: a clinic that serves patients.
  excludes.en    Finance: a department within a company. A department is
                 part of its organization, and is recorded in the module
                 that uses it.
  excludes.en    Rental: a group of renters who arrive together but do not
                 act as one party.
  similar        https://schema.org/Organization
```
