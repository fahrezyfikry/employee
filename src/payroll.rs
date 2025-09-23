use crate::employee::{Employee, FulltimeEmployee, ContractEmployee};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EmployeeData {
    Fulltime(FulltimeEmployee),
    Contract(ContractEmployee),
}

impl EmployeeData {
    pub fn as_employee(&self) -> &dyn Employee {
        match self {
            EmployeeData::Fulltime(emp) => emp,
            EmployeeData::Contract(emp) => emp,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PayrollData {
    pub employee: EmployeeData,
    pub pay_period: String,
    pub processed_date: DateTime<Utc>,
    pub gross_salary: f64,
    pub deductions: f64,
    pub net_salary: f64,
}

impl PayrollData {
    pub fn new(employee: EmployeeData, pay_period: String) -> Self {
        let emp_ref = employee.as_employee();
        let gross_salary = emp_ref.calculate_gross();
        let deductions = emp_ref.calculate_deduction();
        let net_salary = emp_ref.calculate_net();

        Self {
            employee,
            pay_period,
            processed_date: Utc::now(),
            gross_salary,
            deductions,
            net_salary,
        }
    }
}

#[derive(Debug, Default)]
pub struct Payroll {
    pub payroll_records: Vec<PayrollData>,
}

impl Payroll {
    pub fn new() -> Self {
        Self {
            payroll_records: Vec::new(),
        }
    }

    pub fn process_payroll(&mut self, employee: EmployeeData, pay_period: String) -> PayrollData {
        let payroll_data = PayrollData::new(employee, pay_period);
        self.payroll_records.push(payroll_data.clone());
        payroll_data
    }

    pub fn get_payroll_records(&self) -> &Vec<PayrollData> {
        &self.payroll_records
    }

    pub fn get_employee_payroll(&self, employee_id: &str) -> Vec<&PayrollData> {
        self.payroll_records
            .iter()
            .filter(|record| record.employee.as_employee().employee_id() == employee_id)
            .collect()
    }
}

pub struct PayrollPresentation;

impl PayrollPresentation {
    pub fn print_payroll_summary(payroll_data: &PayrollData) {
        let employee = payroll_data.employee.as_employee();
        println!("=== Payroll Summary ===");
        println!("Employee ID: {}", employee.employee_id());
        println!("Employee Type: {}", employee.employee_type());
        println!("Pay Period: {}", payroll_data.pay_period);
        println!("Processed Date: {}", payroll_data.processed_date.format("%Y-%m-%d %H:%M:%S"));
        println!("Work Hours: {}", employee.work_hour());
        println!("Gross Salary: Rp {:.2}", payroll_data.gross_salary);
        println!("Deductions: Rp {:.2}", payroll_data.deductions);
        println!("Net Salary: Rp {:.2}", payroll_data.net_salary);
        println!("{}", "-".repeat(40));
    }

    pub fn print_all_payrolls(payroll_records: &[PayrollData]) {
        println!("=== ALL PAYROLL RECORDS ===\n");
        let mut total_gross = 0.0;
        let mut total_net = 0.0;

        for record in payroll_records {
            Self::print_payroll_summary(record);
            total_gross += record.gross_salary;
            total_net += record.net_salary;
            println!();
        }

        println!("=== TOTAL SUMMARY ===");
        println!("Total Employees: {}", payroll_records.len());
        println!("Total Gross Payroll: Rp {:.2}", total_gross);
        println!("Total Net Payroll: Rp {:.2}", total_net);
        println!("Total Deductions: Rp {:.2}", total_gross - total_net);
    }
}