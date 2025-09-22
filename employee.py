"""
Employee Management System

This module provides a comprehensive employee management system that supports
different types of employees with flexible tax calculation strategies.

Classes:
    Tax: Abstract base class for tax calculation strategies
    Employee: Abstract base class for all employee types
    FulltimeTax: Tax calculation implementation for fulltime employees
    ContractTax: Tax calculation implementation for contract employees
    FulltimeEmployee: Fulltime employee implementation
    ContractEmployee: Contract employee implementation
    PayrollData: Data structure for storing payroll information
    Payroll: Main payroll processing system
    PayrollPresentation: Presentation layer for payroll data

Example:
    >>> fulltime_emp = FulltimeEmployee("FT001", 180, 2000000, "monthly", 8000000, FulltimeTax())
    >>> payroll = Payroll()
    >>> payroll_data = payroll.process_payroll(fulltime_emp, "September 2024")
    >>> PayrollPresentation.print_payroll_summary(payroll_data)
"""

from abc import ABC, abstractmethod
from typing import Union, List
from datetime import datetime


class Tax(ABC):
    """
    Abstract base class for tax calculation strategies.
    
    This class defines the interface for different tax calculation methods
    that can be used by different employee types.
    """
    
    @abstractmethod
    def calculate_tax(self, gross_salary: float) -> float:
        """
        Calculate tax based on gross salary.
        
        Args:
            gross_salary (float): The gross salary amount
            
        Returns:
            float: The calculated tax amount
        """
        pass


class Employee(ABC):
    """
    Abstract base class for all employee types.
    
    This class defines the common interface and properties for all employee types
    in the system. It uses dependency injection for tax calculation strategies.
    
    Attributes:
        employee_id (str): Unique identifier for the employee
        work_hour (float): Number of work hours
        tunjangan (float): Allowance amount
        periode_tunjangan (str): Period of allowance (monthly, yearly, per_project)
    """
    
    def __init__(self, employee_id: str, work_hour: float, tunjangan: float, periode_tunjangan: str):
        """
        Initialize Employee with basic information.
        
        Args:
            employee_id (str): Unique identifier for the employee
            work_hour (float): Number of work hours
            tunjangan (float): Allowance amount
            periode_tunjangan (str): Period of allowance
        """
        self.employee_id = employee_id
        self.work_hour = work_hour
        self.tunjangan = tunjangan
        self.periode_tunjangan = periode_tunjangan
    
    @abstractmethod
    def calculate_gross(self) -> float:
        """
        Calculate gross salary including base salary, overtime, and allowances.
        
        Returns:
            float: The calculated gross salary
        """
        pass
    
    @abstractmethod
    def calculate_deduction(self) -> float:
        """
        Calculate total deductions including tax and other deductions.
        
        Returns:
            float: The calculated total deductions
        """
        pass
    
    @abstractmethod
    def calculate_net(self) -> float:
        """
        Calculate net salary after deductions.
        
        Returns:
            float: The calculated net salary
        """
        pass

class FulltimeTax(Tax):
    def calculate_tax(self, gross_salary: float) -> float:
        if gross_salary <= 54000000:
            return gross_salary * 0.05
        elif gross_salary <= 250000000:
            return gross_salary * 0.15
        elif gross_salary <= 500000000:
            return gross_salary * 0.25
        else:
            return gross_salary * 0.30


class FulltimeEmployee(Employee):
    def __init__(self, employee_id: str, work_hour: float, tunjangan: float, periode_tunjangan: str, base_salary: float, tax_calculator: Tax):
        super().__init__(employee_id, work_hour, tunjangan, periode_tunjangan)
        self.base_salary = base_salary
        self.tax_calculator = tax_calculator
    
    def calculate_gross(self) -> float:
        monthly_salary = self.base_salary
        overtime_rate = self.base_salary / 173
        overtime_hours = max(0, self.work_hour - 173)
        overtime_pay = overtime_hours * overtime_rate * 1.5
        
        if self.periode_tunjangan == "monthly":
            monthly_tunjangan = self.tunjangan
        elif self.periode_tunjangan == "yearly":
            monthly_tunjangan = self.tunjangan / 12
        else:
            monthly_tunjangan = 0
            
        return monthly_salary + overtime_pay + monthly_tunjangan
    
    def calculate_deduction(self) -> float:
        gross = self.calculate_gross()
        tax = self.tax_calculator.calculate_tax(gross * 12) / 12
        bpjs_kesehatan = gross * 0.01
        bpjs_ketenagakerjaan = gross * 0.02
        return tax + bpjs_kesehatan + bpjs_ketenagakerjaan
    
    def calculate_net(self) -> float:
        return self.calculate_gross() - self.calculate_deduction()


class ContractTax(Tax):
    def calculate_tax(self, gross_salary: float) -> float:
        return gross_salary * 0.025


class ContractEmployee(Employee):
    def __init__(self, employee_id: str, work_hour: float, tunjangan: float, periode_tunjangan: str, hourly_rate: float, tax_calculator: Tax):
        super().__init__(employee_id, work_hour, tunjangan, periode_tunjangan)
        self.hourly_rate = hourly_rate
        self.tax_calculator = tax_calculator
    
    def calculate_gross(self) -> float:
        base_pay = self.work_hour * self.hourly_rate
        
        if self.periode_tunjangan == "monthly":
            monthly_tunjangan = self.tunjangan
        elif self.periode_tunjangan == "yearly":
            monthly_tunjangan = self.tunjangan / 12
        elif self.periode_tunjangan == "per_project":
            monthly_tunjangan = self.tunjangan
        else:
            monthly_tunjangan = 0
            
        return base_pay + monthly_tunjangan
    
    def calculate_deduction(self) -> float:
        gross = self.calculate_gross()
        tax = self.tax_calculator.calculate_tax(gross)
        return tax
    
    def calculate_net(self) -> float:
        return self.calculate_gross() - self.calculate_deduction()


class PayrollData:
    def __init__(self, employee: Employee, pay_period: str, processed_date: datetime):
        self.employee = employee
        self.pay_period = pay_period
        self.processed_date = processed_date
        self.gross_salary = employee.calculate_gross()
        self.deductions = employee.calculate_deduction()
        self.net_salary = employee.calculate_net()


class Payroll:
    def __init__(self):
        self.payroll_records: List[PayrollData] = []
    
    def process_payroll(self, employee: Employee, pay_period: str) -> PayrollData:
        payroll_data = PayrollData(
            employee=employee,
            pay_period=pay_period,
            processed_date=datetime.now()
        )
        self.payroll_records.append(payroll_data)
        return payroll_data
    
    def get_payroll_records(self) -> List[PayrollData]:
        return self.payroll_records
    
    def get_employee_payroll(self, employee_id: str) -> List[PayrollData]:
        return [record for record in self.payroll_records if record.employee.employee_id == employee_id]


class PayrollPresentation:
    @staticmethod
    def print_payroll_summary(payroll_data: PayrollData):
        print(f"=== Payroll Summary ===")
        print(f"Employee ID: {payroll_data.employee.employee_id}")
        print(f"Employee Type: {type(payroll_data.employee).__name__}")
        print(f"Pay Period: {payroll_data.pay_period}")
        print(f"Processed Date: {payroll_data.processed_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Work Hours: {payroll_data.employee.work_hour}")
        print(f"Gross Salary: Rp {payroll_data.gross_salary:,.2f}")
        print(f"Deductions: Rp {payroll_data.deductions:,.2f}")
        print(f"Net Salary: Rp {payroll_data.net_salary:,.2f}")
        print("-" * 40)
    
    @staticmethod
    def print_all_payrolls(payroll_records: List[PayrollData]):
        print("=== ALL PAYROLL RECORDS ===\n")
        total_gross = 0
        total_net = 0
        
        for record in payroll_records:
            PayrollPresentation.print_payroll_summary(record)
            total_gross += record.gross_salary
            total_net += record.net_salary
            print()
        
        print(f"=== TOTAL SUMMARY ===")
        print(f"Total Employees: {len(payroll_records)}")
        print(f"Total Gross Payroll: Rp {total_gross:,.2f}")
        print(f"Total Net Payroll: Rp {total_net:,.2f}")
        print(f"Total Deductions: Rp {total_gross - total_net:,.2f}")


if __name__ == "__main__":
    print("=== Employee Management System Demo ===\n")
    
    # Create employees
    fulltime_emp = FulltimeEmployee(
        employee_id="FT001",
        work_hour=180,  # 180 hours in a month (with 7 hours overtime)
        tunjangan=2000000,  # 2 juta tunjangan
        periode_tunjangan="monthly",
        base_salary=8000000,  # 8 juta base salary
        tax_calculator=FulltimeTax()
    )
    
    contract_emp = ContractEmployee(
        employee_id="CT001",
        work_hour=120,  # 120 hours in a month
        tunjangan=1000000,  # 1 juta tunjangan per project
        periode_tunjangan="per_project",
        hourly_rate=75000,  # 75k per hour
        tax_calculator=ContractTax()
    )
    
    # Another contract employee
    contract_emp2 = ContractEmployee(
        employee_id="CT002",
        work_hour=160,
        tunjangan=500000,
        periode_tunjangan="monthly",
        hourly_rate=50000,
        tax_calculator=ContractTax()
    )
    
    # Create payroll system
    payroll = Payroll()
    presentation = PayrollPresentation()
    
    print("=== Processing Payroll ===\n")
    
    # Process payroll for each employee
    ft_payroll = payroll.process_payroll(fulltime_emp, "September 2024")
    ct_payroll = payroll.process_payroll(contract_emp, "September 2024")
    ct2_payroll = payroll.process_payroll(contract_emp2, "September 2024")
    
    # Display individual payroll summaries
    presentation.print_payroll_summary(ft_payroll)
    print()
    presentation.print_payroll_summary(ct_payroll)
    print()
    presentation.print_payroll_summary(ct2_payroll)
    print()
    
    # Display all payrolls with total summary
    presentation.print_all_payrolls(payroll.get_payroll_records())
    
    print("\n=== System supports extensibility for new employee types ===")
    print("To add new employee types, simply:")
    print("1. Create a new Tax class inheriting from Tax")
    print("2. Create a new Employee class inheriting from Employee")
    print("3. Implement the required abstract methods")