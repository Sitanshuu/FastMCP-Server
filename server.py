from fastmcp import FastMCP
from datetime import date, datetime


# Creating a MCP server..
mcp = FastMCP("LeaveManager")

# Mocking data from the database..
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []}
}


# Date validation function used in 'applyLeave' function..
def validate_date_str(date_str: str) -> bool:
    """
    Accepts a string in 'DD-MM-YYYY' format.
    Validates:
    - within allowed ranges (1=>31, 1=>12, 2000=>2050)
    - valid calendar date
    - not in the past
    """
    try:
        # Try to parse the string; this also checks if the date is real
        d = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        # Wrong format or impossible date
        return False
    # Range checks on year
    if not (2000 <= d.year <= 2050):
        return False
    # Past date check
    if d < date.today():
        return False
    return True


# Tool to check leave balance..
@mcp.tool()
def checkLeaveBalance (employee_id: str) -> str:
    """
    This function takes input of an 'employee_id' as string and then checks if the employee
    exists in the mock database 'employee_leaves' and then returns the employee's 
    leave detais as a string.
    """
    data = employee_leaves[employee_id]
    if data:
        return f"Employee with employee id: {employee_id} have {data.get("balance")} leave days left. HISTORY: {data.get("history")}"
    
    return f"Employee with employee id: {employee_id} not found."


# Tool to apply for leave..
@mcp.tool()
def applyLeave (employee_id: str, leave_date: str) -> str:
    """
    This function takes input of an 'employee_id' as string and 'leave_date' as string too
    and then pass the 'leave_date' to the boolean validation function 'validate_date_str'.
    If the validation is true and the employee's balance is greater than or equal to 1,
    it manipulates the mockup data 'employee_leaves' and returns the string about the leave
    details.
    """
    employee_detail = employee_leaves[employee_id]
    if (validate_date_str(leave_date) and employee_detail["balance"]>=1):
        employee_detail["balance"] -= 1
        employee_detail["history"].append(leave_date)
        return f"Leave granted to employee with employee id: {employee_id}; Updated Remaining Balance: {employee_detail.get("balance")}; Updated History: {employee_detail.get("history")}"

    return f"Employee with employee id: {employee_id} cannot take a leave."


# Tool to check the leave history..
@mcp.tool()
def getLeaveHistory (employee_id: str) -> str:
    """
    This function takes input of an 'employee_id' as string and then checks if the employee
    exists in the mock database 'employee_leaves' and then returns the leave history
    as a string.
    """
    data = employee_leaves[employee_id]
    if data:
        return f"Employee id: {employee_id}; HISTORY: {data.get("history")}"
    
    return "Employee with employee id: {employee_id} not found nor have any history."


# Resource: Greeting..
@mcp.resource("greeting://{name}")
def getGreeting(name: str) -> str:
    """
    This is a greeting function that takes input of a 'name' as string and returns a
    string greeting.
    """
    return f"Hello, {name}! How can I assist you with leave management today?"


if (__name__ == "__main__"):
    mcp.run()