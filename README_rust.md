# Employee Management System (Rust CLI)

This is a Rust CLI application converted from the original Python employee management system. It provides a comprehensive employee management system with tax calculation and payroll processing.

## Features

- **Employee Management**: Add fulltime and contract employees
- **Tax Calculation**: Automatic tax calculation based on employee type
- **Payroll Processing**: Process payroll with detailed breakdowns
- **Interactive CLI**: Menu-driven interface for easy navigation
- **Data Persistence**: Maintains records during the session

## Installation

Make sure you have Rust installed on your system. If not, install it from [rustup.rs](https://rustup.rs/).

1. Clone or download the project
2. Navigate to the project directory
3. Build the project:

```bash
cargo build --release
```

## Usage

Run the application:

```bash
cargo run
```

### Menu Options

1. **Add Fulltime Employee**
   - Enter employee details including ID, work hours, allowances, and base salary
   - Automatic overtime calculation for hours over 173
   - Progressive tax rates and BPJS deductions

2. **Add Contract Employee**
   - Enter employee details including ID, work hours, allowances, and hourly rate
   - Flat tax rate of 2.5%
   - Project-based allowance support

3. **Process Payroll**
   - Create payroll records for employees
   - Real-time calculation of gross, deductions, and net salary
   - Immediate payroll summary display

4. **Show All Payrolls**
   - Display all processed payroll records
   - Total summary with aggregate statistics

5. **Show Employee Payroll**
   - View payroll history for a specific employee
   - Filter by employee ID

6. **Exit**
   - Close the application

### Employee Types

#### Fulltime Employee
- **Base Salary**: Fixed monthly salary
- **Overtime**: 1.5x rate for hours over 173
- **Tax Rates**: Progressive (5%, 15%, 25%, 30%)
- **Deductions**: Tax + BPJS Kesehatan (1%) + BPJS Ketenagakerjaan (2%)

#### Contract Employee  
- **Hourly Rate**: Payment based on hours worked
- **Tax Rate**: Flat 2.5%
- **Allowances**: Support for monthly, yearly, or per-project allowances

### Allowance Periods
- **Monthly**: Applied every month
- **Yearly**: Divided by 12 for monthly calculation
- **Per Project**: Applied once per project (for contracts)

## Example Usage

```
=== Employee Management System ===

=== MAIN MENU ===
1. Add Fulltime Employee
2. Add Contract Employee
3. Process Payroll
4. Show All Payrolls
5. Show Employee Payroll
6. Exit

Enter your choice: 3

=== Process Payroll ===
Employee Type (fulltime/contract): fulltime
Employee ID: FT001
Work Hours: 180
Allowance (Tunjangan): 2000000
Allowance Period (monthly/yearly/per_project): monthly
Pay Period (e.g., 'September 2024'): September 2024
Base Salary: 8000000

Payroll processed successfully!
=== Payroll Summary ===
Employee ID: FT001
Employee Type: FulltimeEmployee
Pay Period: September 2024
Processed Date: 2024-09-23 14:35:22
Work Hours: 180
Gross Salary: Rp 10637500.00
Deductions: Rp 797812.50
Net Salary: Rp 9839687.50
```

## Architecture

The application is structured with the following modules:

- **`tax.rs`**: Tax calculation strategies (Strategy pattern)
- **`employee.rs`**: Employee types and calculations (Abstract factory pattern)
- **`payroll.rs`**: Payroll processing and data management
- **`cli.rs`**: Command-line interface and user interaction
- **`main.rs`**: Application entry point

## Dependencies

- `chrono`: Date/time handling
- `serde`: Serialization support (future persistence features)
- `serde_json`: JSON serialization

## Build Commands

```bash
# Development build
cargo build

# Release build (optimized)
cargo build --release

# Run the application
cargo run

# Run tests (if any)
cargo test
```

## Future Enhancements

- File-based persistence (JSON/CSV export)
- Employee search and filtering
- Bulk payroll processing
- Report generation
- Configuration file support
