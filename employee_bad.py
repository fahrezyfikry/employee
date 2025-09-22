"""
Bad Employee Management System - Example of Poor Design

This module demonstrates poor design practices including:
- No separation of concerns
- Tight coupling
- Violation of Single Responsibility Principle
- No abstraction or polymorphism
- Hard to maintain and extend
"""

def calculate_payroll(employee_type, employee_id, work_hour, hourly_rate, salary_type, annual_salary, period):
    """
    One massive function that handles everything!
    """
    
    # Calculate gross salary based on employee type
    if employee_type == "fulltime":
        if salary_type == "monthly":
            gross_salary = annual_salary / 12
        elif salary_type == "weekly":
            gross_salary = annual_salary / 52
        else:
            gross_salary = annual_salary / 365
            
        # Fulltime tax calculation mixed in
        if gross_salary <= 5000000:
            tax_rate = 0.05
        elif gross_salary <= 10000000:
            tax_rate = 0.10
        elif gross_salary <= 20000000:
            tax_rate = 0.15
        else:
            tax_rate = 0.20
            
        tax_amount = gross_salary * tax_rate
        
        # Fulltime benefits calculation
        health_insurance = 500000
        transport_allowance = 300000
        meal_allowance = 200000
        total_benefits = health_insurance + transport_allowance + meal_allowance
        
    elif employee_type == "contract":
        # Contract salary calculation
        gross_salary = work_hour * hourly_rate
        
        # Contract tax calculation - different logic but all in one place
        if gross_salary <= 3000000:
            tax_rate = 0.02
        elif gross_salary <= 8000000:
            tax_rate = 0.08
        elif gross_salary <= 15000000:
            tax_rate = 0.12
        else:
            tax_rate = 0.18
            
        tax_amount = gross_salary * tax_rate
        
        # Contract benefits - minimal
        health_insurance = 200000
        transport_allowance = 0
        meal_allowance = 0
        total_benefits = health_insurance
        
    else:
        # No proper error handling
        print("Unknown employee type!")
        return None
    
    # Calculate net salary
    net_salary = gross_salary - tax_amount + total_benefits
    
    # Generate payroll data
    payroll_result = {
        "employee_id": employee_id,
        "employee_type": employee_type,
        "period": period,
        "work_hour": work_hour,
        "hourly_rate": hourly_rate,
        "gross_salary": gross_salary,
        "tax_amount": tax_amount,
        "health_insurance": health_insurance,
        "transport_allowance": transport_allowance,
        "meal_allowance": meal_allowance,
        "total_benefits": total_benefits,
        "net_salary": net_salary,
        "processed_date": "2024-09-22"
    }
    
    return payroll_result


def print_payroll_bad(payroll_data):
    """
    Poor presentation logic mixed with business logic
    """
    if payroll_data is None:
        print("No payroll data to display!")
        return
        
    print("=" * 50)
    print("PAYROLL SUMMARY")
    print("=" * 50)
    print(f"Employee ID: {payroll_data['employee_id']}")
    print(f"Employee Type: {payroll_data['employee_type']}")
    print(f"Period: {payroll_data['period']}")
    print(f"Work Hours: {payroll_data['work_hour']}")
    print(f"Hourly Rate: Rp {payroll_data['hourly_rate']:,.2f}")
    print("-" * 30)
    print(f"Gross Salary: Rp {payroll_data['gross_salary']:,.2f}")
    print(f"Tax Amount: Rp {payroll_data['tax_amount']:,.2f}")
    print(f"Health Insurance: Rp {payroll_data['health_insurance']:,.2f}")
    print(f"Transport Allowance: Rp {payroll_data['transport_allowance']:,.2f}")
    print(f"Meal Allowance: Rp {payroll_data['meal_allowance']:,.2f}")
    print(f"Total Benefits: Rp {payroll_data['total_benefits']:,.2f}")
    print("-" * 30)
    print(f"NET SALARY: Rp {payroll_data['net_salary']:,.2f}")
    print(f"Processed Date: {payroll_data['processed_date']}")
    print("=" * 50)


# Example usage with poor structure
if __name__ == "__main__":
    # Process fulltime employee
    ft_payroll = calculate_payroll(
        "fulltime", "FT001", 180, 2000000, "monthly", 8000000, "September 2024"
    )
    print_payroll_bad(ft_payroll)
    
    print("\n")
    
    # Process contract employee
    ct_payroll = calculate_payroll(
        "contract", "CT001", 120, 50000, "hourly", 0, "September 2024"
    )
    print_payroll_bad(ct_payroll)
    
    # What happens with invalid employee type?
    invalid_payroll = calculate_payroll(
        "intern", "IN001", 100, 25000, "hourly", 0, "September 2024"
    )
    print_payroll_bad(invalid_payroll)