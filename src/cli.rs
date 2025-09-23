use crate::employee::{AllowancePeriod, ContractEmployee, FulltimeEmployee};
use crate::payroll::{EmployeeData, Payroll, PayrollPresentation};
use std::io::{self, Write};

pub struct CLI {
    payroll: Payroll,
}

impl CLI {
    pub fn new() -> Self {
        Self {
            payroll: Payroll::new(),
        }
    }

    pub fn run(&mut self) {
        println!("=== Employee Management System ===\n");
        
        loop {
            self.show_menu();
            let choice = self.get_input("Enter your choice: ");
            
            match choice.trim() {
                "1" => self.add_fulltime_employee(),
                "2" => self.add_contract_employee(),
                "3" => self.process_payroll(),
                "4" => self.show_all_payrolls(),
                "5" => self.show_employee_payroll(),
                "6" => {
                    println!("Thank you for using Employee Management System!");
                    break;
                }
                _ => println!("Invalid choice. Please try again.\n"),
            }
        }
    }

    fn show_menu(&self) {
        println!("=== MAIN MENU ===");
        println!("1. Add Fulltime Employee");
        println!("2. Add Contract Employee");
        println!("3. Process Payroll");
        println!("4. Show All Payrolls");
        println!("5. Show Employee Payroll");
        println!("6. Exit");
        println!();
    }

    fn get_input(&self, prompt: &str) -> String {
        print!("{}", prompt);
        io::stdout().flush().unwrap();
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        input
    }

    fn get_number_input(&self, prompt: &str) -> Result<f64, std::num::ParseFloatError> {
        let input = self.get_input(prompt);
        input.trim().parse::<f64>()
    }

    fn add_fulltime_employee(&mut self) {
        println!("\n=== Add Fulltime Employee ===");
        
        let employee_id = self.get_input("Employee ID: ").trim().to_string();
        
        let work_hour = loop {
            match self.get_number_input("Work Hours: ") {
                Ok(hours) if hours >= 0.0 => break hours,
                _ => println!("Please enter a valid positive number for work hours."),
            }
        };
        
        let tunjangan = loop {
            match self.get_number_input("Allowance (Tunjangan): ") {
                Ok(amount) if amount >= 0.0 => break amount,
                _ => println!("Please enter a valid positive number for allowance."),
            }
        };
        
        let periode_tunjangan = loop {
            let period = self.get_input("Allowance Period (monthly/yearly/per_project): ");
            match AllowancePeriod::from_str(period.trim()) {
                Some(period) => break period,
                None => println!("Please enter 'monthly', 'yearly', or 'per_project'."),
            }
        };
        
        let base_salary = loop {
            match self.get_number_input("Base Salary: ") {
                Ok(salary) if salary > 0.0 => break salary,
                _ => println!("Please enter a valid positive number for base salary."),
            }
        };

        let employee = FulltimeEmployee::new(
            employee_id,
            work_hour,
            tunjangan,
            periode_tunjangan,
            base_salary,
        );

        println!("Fulltime employee added successfully!\n");
    }

    fn add_contract_employee(&mut self) {
        println!("\n=== Add Contract Employee ===");
        
        let employee_id = self.get_input("Employee ID: ").trim().to_string();
        
        let work_hour = loop {
            match self.get_number_input("Work Hours: ") {
                Ok(hours) if hours >= 0.0 => break hours,
                _ => println!("Please enter a valid positive number for work hours."),
            }
        };
        
        let tunjangan = loop {
            match self.get_number_input("Allowance (Tunjangan): ") {
                Ok(amount) if amount >= 0.0 => break amount,
                _ => println!("Please enter a valid positive number for allowance."),
            }
        };
        
        let periode_tunjangan = loop {
            let period = self.get_input("Allowance Period (monthly/yearly/per_project): ");
            match AllowancePeriod::from_str(period.trim()) {
                Some(period) => break period,
                None => println!("Please enter 'monthly', 'yearly', or 'per_project'."),
            }
        };
        
        let hourly_rate = loop {
            match self.get_number_input("Hourly Rate: ") {
                Ok(rate) if rate > 0.0 => break rate,
                _ => println!("Please enter a valid positive number for hourly rate."),
            }
        };

        let employee = ContractEmployee::new(
            employee_id,
            work_hour,
            tunjangan,
            periode_tunjangan,
            hourly_rate,
        );

        println!("Contract employee added successfully!\n");
    }

    fn process_payroll(&mut self) {
        println!("\n=== Process Payroll ===");
        
        let employee_type = loop {
            let input = self.get_input("Employee Type (fulltime/contract): ");
            match input.trim().to_lowercase().as_str() {
                "fulltime" | "ft" => break "fulltime",
                "contract" | "ct" => break "contract",
                _ => println!("Please enter 'fulltime' or 'contract'."),
            }
        };

        let employee_id = self.get_input("Employee ID: ").trim().to_string();
        let work_hour = loop {
            match self.get_number_input("Work Hours: ") {
                Ok(hours) if hours >= 0.0 => break hours,
                _ => println!("Please enter a valid positive number for work hours."),
            }
        };
        
        let tunjangan = loop {
            match self.get_number_input("Allowance (Tunjangan): ") {
                Ok(amount) if amount >= 0.0 => break amount,
                _ => println!("Please enter a valid positive number for allowance."),
            }
        };
        
        let periode_tunjangan = loop {
            let period = self.get_input("Allowance Period (monthly/yearly/per_project): ");
            match AllowancePeriod::from_str(period.trim()) {
                Some(period) => break period,
                None => println!("Please enter 'monthly', 'yearly', or 'per_project'."),
            }
        };

        let pay_period = self.get_input("Pay Period (e.g., 'September 2024'): ").trim().to_string();

        let employee_data = if employee_type == "fulltime" {
            let base_salary = loop {
                match self.get_number_input("Base Salary: ") {
                    Ok(salary) if salary > 0.0 => break salary,
                    _ => println!("Please enter a valid positive number for base salary."),
                }
            };

            let employee = FulltimeEmployee::new(
                employee_id,
                work_hour,
                tunjangan,
                periode_tunjangan,
                base_salary,
            );
            EmployeeData::Fulltime(employee)
        } else {
            let hourly_rate = loop {
                match self.get_number_input("Hourly Rate: ") {
                    Ok(rate) if rate > 0.0 => break rate,
                    _ => println!("Please enter a valid positive number for hourly rate."),
                }
            };

            let employee = ContractEmployee::new(
                employee_id,
                work_hour,
                tunjangan,
                periode_tunjangan,
                hourly_rate,
            );
            EmployeeData::Contract(employee)
        };

        let payroll_data = self.payroll.process_payroll(employee_data, pay_period);
        
        println!("\nPayroll processed successfully!");
        PayrollPresentation::print_payroll_summary(&payroll_data);
        println!();
    }

    fn show_all_payrolls(&self) {
        println!("\n=== All Payroll Records ===");
        
        if self.payroll.payroll_records.is_empty() {
            println!("No payroll records found.\n");
            return;
        }

        PayrollPresentation::print_all_payrolls(&self.payroll.payroll_records);
        println!();
    }

    fn show_employee_payroll(&self) {
        println!("\n=== Employee Payroll History ===");
        
        if self.payroll.payroll_records.is_empty() {
            println!("No payroll records found.\n");
            return;
        }

        let employee_id = self.get_input("Enter Employee ID: ").trim().to_string();
        let records = self.payroll.get_employee_payroll(&employee_id);
        
        if records.is_empty() {
            println!("No payroll records found for employee ID: {}\n", employee_id);
            return;
        }

        println!("Payroll records for employee {}:\n", employee_id);
        for record in records {
            PayrollPresentation::print_payroll_summary(record);
            println!();
        }
    }
}