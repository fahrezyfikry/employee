from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class LibraryError(Exception):
    """Base error for library domain."""


class BookNotFoundError(LibraryError):
    """Raised when a book is not found in the library."""


class MemberNotFoundError(LibraryError):
    """Raised when a member is not found in the library."""


class BookUnavailableError(LibraryError):
    """Raised when trying to borrow a book that is not available."""


class BookNotBorrowedError(LibraryError):
    """Raised when trying to return a book that is not currently borrowed."""


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


@dataclass
class Buku:
    """
    Book entity.

    Attributes:
    - id_buku: unique identifier of the book in the library
    - judul: book title
    - penulis: author name
    - status: availability status (AVAILABLE | BORROWED)
    - dipinjam_oleh: member id currently borrowing the book (if any)
    """

    id_buku: str
    judul: str
    penulis: str
    status: BookStatus = BookStatus.AVAILABLE
    dipinjam_oleh: Optional[str] = None

    def tersedia(self) -> bool:
        """Return True if this book is available to borrow."""
        return self.status is BookStatus.AVAILABLE


@dataclass
class Anggota:
    """
    Member entity.

    Attributes:
    - idAnggota: unique identifier for the member
    - nama: member name
    - buku_dipinjam: list of book ids currently borrowed by this member
    """

    idAnggota: str
    nama: str
    buku_dipinjam: List[str] = field(default_factory=list)

    # Per requirement, methods live on the Anggota class
    def pinjamBuku(self, perpustakaan: "Perpustakaan", id_buku: str) -> None:
        """
        Borrow a book from the library for this member.

        Preconditions:
        - Member is registered in the library
        - Book exists in the library and is available

        Postconditions:
        - Buku.status == BORROWED
        - Buku.dipinjam_oleh == self.idAnggota
        - id_buku is appended to self.buku_dipinjam
        """
        perpustakaan.pinjam_buku(self.idAnggota, id_buku)

    def kembalikanBuku(self, perpustakaan: "Perpustakaan", id_buku: str) -> None:
        """
        Return a book to the library by this member.

        Preconditions:
        - Member is registered in the library
        - The book is currently borrowed and borrowed by this member

        Postconditions:
        - Buku.status == AVAILABLE
        - Buku.dipinjam_oleh == None
        - id_buku is removed from self.buku_dipinjam
        """
        perpustakaan.kembalikan_buku(self.idAnggota, id_buku)


class Perpustakaan:
    """
    Manage book and member collections as well as borrow/return processes.

    OOD principles:
    - Single Responsibility: focuses on orchestrating book/member state.
    - Encapsulation: state changes via clear public methods.
    - Abstraction: validation details hidden behind a simple API.
    - Extensibility: easy to extend (e.g., quotas, fines).
    """

    def __init__(self) -> None:
        self._buku: Dict[str, Buku] = {}
        self._anggota: Dict[str, Anggota] = {}

    # Basic data management
    def tambah_buku(self, buku: Buku) -> None:
        self._buku[buku.id_buku] = buku

    def tambah_anggota(self, anggota: Anggota) -> None:
        self._anggota[anggota.idAnggota] = anggota

    def cari_buku(self, id_buku: str) -> Buku:
        buku = self._buku.get(id_buku)
        if buku is None:
            raise BukuTidakDitemukanError(f"Buku dengan id '{id_buku}' tidak ditemukan")
        return buku

    def cari_anggota(self, id_anggota: str) -> Anggota:
        anggota = self._anggota.get(id_anggota)
        if anggota is None:
            raise AnggotaTidakDitemukanError(
                f"Anggota dengan id '{id_anggota}' tidak ditemukan"
            )
        return anggota

    # Business processes
    def pinjam_buku(self, id_anggota: str, id_buku: str) -> None:
        """
        Book borrowing process.

        Preconditions:
        - Book is available
        - Member is registered

        Postconditions:
        - Buku.status == BORROWED and dipinjam_oleh == id_anggota
        - id_buku is added to the member's buku_dipinjam list
        """
        anggota = self.cari_anggota(id_anggota)
        buku = self.cari_buku(id_buku)

        if not buku.tersedia():
            raise BukuTidakTersediaError(
                f"Buku '{buku.judul}' sedang tidak tersedia untuk dipinjam"
            )

        # Centralized state mutation in Perpustakaan to keep consistency
        buku.status = BookStatus.BORROWED
        buku.dipinjam_oleh = anggota.idAnggota
        if id_buku not in anggota.buku_dipinjam:
            anggota.buku_dipinjam.append(id_buku)

        # Postconditions (defensive checks - can be removed if unnecessary)
        assert not buku.tersedia()
        assert buku.dipinjam_oleh == anggota.idAnggota
        assert id_buku in anggota.buku_dipinjam

    def kembalikan_buku(self, id_anggota: str, id_buku: str) -> None:
        """
        Book return process.

        Preconditions:
        - Book is currently BORROWED and borrowed by id_anggota
        - Member is registered

        Postconditions:
        - Buku.status == AVAILABLE and dipinjam_oleh == None
        - id_buku is removed from the member's buku_dipinjam list
        """
        anggota = self.cari_anggota(id_anggota)
        buku = self.cari_buku(id_buku)

        if buku.status is not BookStatus.BORROWED or buku.dipinjam_oleh != id_anggota:
            raise BukuTidakSedangDipinjamError(
                f"Buku '{buku.judul}' tidak sedang dipinjam oleh anggota ini"
            )

        # State mutation
        buku.status = BookStatus.AVAILABLE
        buku.dipinjam_oleh = None
        if id_buku in anggota.buku_dipinjam:
            anggota.buku_dipinjam.remove(id_buku)

        # Postconditions
        assert buku.tersedia()
        assert buku.dipinjam_oleh is None
        assert id_buku not in anggota.buku_dipinjam


if __name__ == "__main__":
    # Minimal demonstration of borrow/return flow
    lib = Perpustakaan()
    lib.tambah_buku(Buku(id_buku="B1", judul="Clean Code", penulis="Robert C. Martin"))
    lib.tambah_buku(
        Buku(id_buku="B2", judul="The Pragmatic Programmer", penulis="Andrew Hunt")
    )
    lib.tambah_anggota(Anggota(idAnggota="A1", nama="Andi"))

    anggota = lib.cari_anggota("A1")
    print("Sebelum dipinjam:", lib.cari_buku("B1").status)
    anggota.pinjamBuku(lib, "B1")
    print(
        "Setelah dipinjam:",
        lib.cari_buku("B1").status,
        "Dipinjam oleh=",
        lib.cari_buku("B1").dipinjam_oleh,
    )
    anggota.kembalikanBuku(lib, "B1")
    print(
        "Setelah dikembalikan:",
        lib.cari_buku("B1").status,
        "Dipinjam oleh=",
        lib.cari_buku("B1").dipinjam_oleh,
    )


