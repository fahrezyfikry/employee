use crate::tax::Tax;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum AllowancePeriod {
    Monthly,
    Yearly,
    PerProject,
}

impl AllowancePeriod {
    pub fn from_str(s: &str) -> Option<AllowancePeriod> {
        match s.to_lowercase().as_str() {
            "monthly" => Some(AllowancePeriod::Monthly),
            "yearly" => Some(AllowancePeriod::Yearly),
            "per_project" => Some(AllowancePeriod::PerProject),
            _ => None,
        }
    }
}

pub trait Employee {
    fn employee_id(&self) -> &str;
    fn work_hour(&self) -> f64;
    fn tunjangan(&self) -> f64;
    fn periode_tunjangan(&self) -> &AllowancePeriod;
    fn calculate_gross(&self) -> f64;
    fn calculate_deduction(&self) -> f64;
    fn calculate_net(&self) -> f64;
    fn employee_type(&self) -> &str;
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FulltimeEmployee {
    pub employee_id: String,
    pub work_hour: f64,
    pub tunjangan: f64,
    pub periode_tunjangan: AllowancePeriod,
    pub base_salary: f64,
}

impl FulltimeEmployee {
    pub fn new(
        employee_id: String,
        work_hour: f64,
        tunjangan: f64,
        periode_tunjangan: AllowancePeriod,
        base_salary: f64,
    ) -> Self {
        Self {
            employee_id,
            work_hour,
            tunjangan,
            periode_tunjangan,
            base_salary,
        }
    }
}

impl Employee for FulltimeEmployee {
    fn employee_id(&self) -> &str {
        &self.employee_id
    }

    fn work_hour(&self) -> f64 {
        self.work_hour
    }

    fn tunjangan(&self) -> f64 {
        self.tunjangan
    }

    fn periode_tunjangan(&self) -> &AllowancePeriod {
        &self.periode_tunjangan
    }

    fn calculate_gross(&self) -> f64 {
        let monthly_salary = self.base_salary;
        let overtime_rate = self.base_salary / 173.0;
        let overtime_hours = if self.work_hour > 173.0 { self.work_hour - 173.0 } else { 0.0 };
        let overtime_pay = overtime_hours * overtime_rate * 1.5;

        let monthly_tunjangan = match self.periode_tunjangan {
            AllowancePeriod::Monthly => self.tunjangan,
            AllowancePeriod::Yearly => self.tunjangan / 12.0,
            AllowancePeriod::PerProject => 0.0,
        };

        monthly_salary + overtime_pay + monthly_tunjangan
    }

    fn calculate_deduction(&self) -> f64 {
        let gross = self.calculate_gross();
        let tax_calculator = crate::tax::FulltimeTax;
        let tax = tax_calculator.calculate_tax(gross * 12.0) / 12.0;
        let bpjs_kesehatan = gross * 0.01;
        let bpjs_ketenagakerjaan = gross * 0.02;
        tax + bpjs_kesehatan + bpjs_ketenagakerjaan
    }

    fn calculate_net(&self) -> f64 {
        self.calculate_gross() - self.calculate_deduction()
    }

    fn employee_type(&self) -> &str {
        "FulltimeEmployee"
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContractEmployee {
    pub employee_id: String,
    pub work_hour: f64,
    pub tunjangan: f64,
    pub periode_tunjangan: AllowancePeriod,
    pub hourly_rate: f64,
}

impl ContractEmployee {
    pub fn new(
        employee_id: String,
        work_hour: f64,
        tunjangan: f64,
        periode_tunjangan: AllowancePeriod,
        hourly_rate: f64,
    ) -> Self {
        Self {
            employee_id,
            work_hour,
            tunjangan,
            periode_tunjangan,
            hourly_rate,
        }
    }
}

impl Employee for ContractEmployee {
    fn employee_id(&self) -> &str {
        &self.employee_id
    }

    fn work_hour(&self) -> f64 {
        self.work_hour
    }

    fn tunjangan(&self) -> f64 {
        self.tunjangan
    }

    fn periode_tunjangan(&self) -> &AllowancePeriod {
        &self.periode_tunjangan
    }

    fn calculate_gross(&self) -> f64 {
        let base_pay = self.work_hour * self.hourly_rate;

        let monthly_tunjangan = match self.periode_tunjangan {
            AllowancePeriod::Monthly => self.tunjangan,
            AllowancePeriod::Yearly => self.tunjangan / 12.0,
            AllowancePeriod::PerProject => self.tunjangan,
        };

        base_pay + monthly_tunjangan
    }

    fn calculate_deduction(&self) -> f64 {
        let gross = self.calculate_gross();
        let tax_calculator = crate::tax::ContractTax;
        tax_calculator.calculate_tax(gross)
    }

    fn calculate_net(&self) -> f64 {
        self.calculate_gross() - self.calculate_deduction()
    }

    fn employee_type(&self) -> &str {
        "ContractEmployee"
    }
}