# Sistem Manajemen Pegawai

Sistem manajemen pegawai yang komprehensif dengan dukungan untuk berbagai tipe pegawai dan strategi perhitungan pajak yang fleksibel.

## Fitur Utama

- **Extensible Design**: Mudah menambahkan tipe pegawai baru
- **Dependency Injection**: Strategi perhitungan pajak dapat diubah secara dinamis
- **Comprehensive Payroll**: Sistem payroll lengkap dengan presentasi data
- **Object-Oriented**: Menggunakan prinsip OOP dengan abstract classes dan inheritance

## Struktur Kelas

### Abstract Classes

#### `Tax`
Abstract base class untuk strategi perhitungan pajak.

**Method:**
- `calculate_tax(gross_salary: float) -> float`: Menghitung pajak berdasarkan gaji bruto

#### `Employee`
Abstract base class untuk semua tipe pegawai.

**Atribut:**
- `employee_id`: ID unik pegawai
- `work_hour`: Jam kerja
- `tunjangan`: Jumlah tunjangan
- `periode_tunjangan`: Periode tunjangan (monthly, yearly, per_project)

**Method:**
- `calculate_gross() -> float`: Menghitung gaji bruto
- `calculate_deduction() -> float`: Menghitung total potongan
- `calculate_net() -> float`: Menghitung gaji bersih

### Implementasi Tax

#### `FulltimeTax`
Implementasi perhitungan pajak untuk pegawai tetap dengan tarif progresif:
- ≤ 54 juta: 5%
- ≤ 250 juta: 15%
- ≤ 500 juta: 25%
- > 500 juta: 30%

#### `ContractTax`
Implementasi perhitungan pajak untuk pegawai kontrak dengan tarif flat 2.5%.

### Implementasi Employee

#### `FulltimeEmployee`
Pegawai tetap dengan fitur:
- Gaji pokok bulanan
- Overtime pay (1.5x untuk jam kerja > 173 jam)
- BPJS Kesehatan (1%)
- BPJS Ketenagakerjaan (2%)
- Pajak progresif

**Parameter Constructor:**
- `employee_id`: ID pegawai
- `work_hour`: Jam kerja
- `tunjangan`: Jumlah tunjangan
- `periode_tunjangan`: Periode tunjangan
- `base_salary`: Gaji pokok bulanan
- `tax_calculator`: Strategi perhitungan pajak

#### `ContractEmployee`
Pegawai kontrak dengan fitur:
- Pembayaran per jam
- Tunjangan fleksibel
- Pajak flat rate

**Parameter Constructor:**
- `employee_id`: ID pegawai
- `work_hour`: Jam kerja
- `tunjangan`: Jumlah tunjangan
- `periode_tunjangan`: Periode tunjangan
- `hourly_rate`: Tarif per jam
- `tax_calculator`: Strategi perhitungan pajak

### Sistem Payroll

#### `PayrollData`
Data structure untuk menyimpan informasi payroll:
- `employee`: Objek pegawai
- `pay_period`: Periode pembayaran
- `processed_date`: Tanggal pemrosesan
- `gross_salary`: Gaji bruto
- `deductions`: Total potongan
- `net_salary`: Gaji bersih

#### `Payroll`
Sistem utama untuk mengelola payroll:

**Method:**
- `process_payroll(employee, pay_period)`: Memproses payroll pegawai
- `get_payroll_records()`: Mendapatkan semua record payroll
- `get_employee_payroll(employee_id)`: Mendapatkan payroll berdasarkan ID pegawai

#### `PayrollPresentation`
Layer presentasi untuk menampilkan data payroll:

**Method:**
- `print_payroll_summary(payroll_data)`: Menampilkan ringkasan payroll individual
- `print_all_payrolls(payroll_records)`: Menampilkan semua payroll dengan summary total

## Cara Penggunaan

### 1. Membuat Pegawai

```python
# Pegawai Tetap
fulltime_emp = FulltimeEmployee(
    employee_id="FT001",
    work_hour=180,
    tunjangan=2000000,
    periode_tunjangan="monthly",
    base_salary=8000000,
    tax_calculator=FulltimeTax()
)

# Pegawai Kontrak
contract_emp = ContractEmployee(
    employee_id="CT001",
    work_hour=120,
    tunjangan=1000000,
    periode_tunjangan="per_project",
    hourly_rate=75000,
    tax_calculator=ContractTax()
)
```

### 2. Mengelola Payroll

```python
# Buat sistem payroll
payroll = Payroll()
presentation = PayrollPresentation()

# Proses payroll
ft_payroll = payroll.process_payroll(fulltime_emp, "September 2024")
ct_payroll = payroll.process_payroll(contract_emp, "September 2024")

# Tampilkan hasil
presentation.print_payroll_summary(ft_payroll)
presentation.print_all_payrolls(payroll.get_payroll_records())
```

### 3. Menambah Tipe Pegawai Baru

Untuk menambahkan tipe pegawai baru:

1. **Buat Tax Strategy Baru:**
```python
class FreelanceTax(Tax):
    def calculate_tax(self, gross_salary: float) -> float:
        return gross_salary * 0.015  # 1.5% flat rate
```

2. **Buat Employee Class Baru:**
```python
class FreelanceEmployee(Employee):
    def __init__(self, employee_id: str, work_hour: float, tunjangan: float, 
                 periode_tunjangan: str, project_rate: float, tax_calculator: Tax):
        super().__init__(employee_id, work_hour, tunjangan, periode_tunjangan)
        self.project_rate = project_rate
        self.tax_calculator = tax_calculator
    
    def calculate_gross(self) -> float:
        # Implementasi perhitungan gaji bruto
        pass
    
    def calculate_deduction(self) -> float:
        # Implementasi perhitungan potongan
        pass
    
    def calculate_net(self) -> float:
        return self.calculate_gross() - self.calculate_deduction()
```

## Prinsip Design

### 1. Strategy Pattern
Sistem menggunakan Strategy Pattern untuk perhitungan pajak, memungkinkan algoritma pajak yang berbeda untuk setiap tipe pegawai.

### 2. Dependency Injection
Tax calculator diinjeksi ke dalam constructor employee, bukan di-hardcode, meningkatkan fleksibilitas dan testability.

### 3. Single Responsibility Principle
Setiap class memiliki tanggung jawab yang jelas:
- `Tax`: Perhitungan pajak
- `Employee`: Data dan operasi pegawai
- `Payroll`: Manajemen payroll
- `PayrollPresentation`: Presentasi data

### 4. Open-Closed Principle
Sistem terbuka untuk extension (menambah tipe pegawai baru) namun tertutup untuk modification (tidak perlu mengubah kode yang sudah ada).

## Contoh Output

```
=== Payroll Summary ===
Employee ID: FT001
Employee Type: FulltimeEmployee
Pay Period: September 2024
Processed Date: 2025-09-22 08:32:46
Work Hours: 180
Gross Salary: Rp 10,485,549.13
Deductions: Rp 1,887,398.84
Net Salary: Rp 8,598,150.29
----------------------------------------

=== TOTAL SUMMARY ===
Total Employees: 3
Total Gross Payroll: Rp 28,985,549.13
Total Net Payroll: Rp 26,635,650.29
Total Deductions: Rp 2,349,898.84
```

## Requirements

- Python 3.7+
- Modules: `abc`, `typing`, `datetime`

## Menjalankan Sistem

```bash
python employee.py
```

Perintah ini akan menjalankan demo lengkap sistem dengan contoh pegawai tetap dan kontrak.
