pub trait Tax {
    fn calculate_tax(&self, gross_salary: f64) -> f64;
}

#[derive(Debug, Clone)]
pub struct FulltimeTax;

impl Tax for FulltimeTax {
    fn calculate_tax(&self, gross_salary: f64) -> f64 {
        if gross_salary <= 54_000_000.0 {
            gross_salary * 0.05
        } else if gross_salary <= 250_000_000.0 {
            gross_salary * 0.15
        } else if gross_salary <= 500_000_000.0 {
            gross_salary * 0.25
        } else {
            gross_salary * 0.30
        }
    }
}

#[derive(Debug, Clone)]
pub struct ContractTax;

impl Tax for ContractTax {
    fn calculate_tax(&self, gross_salary: f64) -> f64 {
        gross_salary * 0.025
    }
}