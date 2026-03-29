from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(price_per_night: float, total_days: int) -> float:
            """Calculate total hotel cost by multiplying price per night and total days.
            Args:
                price_per_night (float): Price for one night.
                total_days (int): Number of days staying.
            """
            return self.calculator.multiply(float(price_per_night), int(total_days))
        
        @tool
        def calculate_total_expense(total_accommodation: float, total_food: float, total_transport: float, total_activities: float) -> float:
            """Calculate the grand total of the trip by summing all costs.
            Args:
                total_accommodation (float): Total hotel/stay cost.
                total_food (float): Total food cost.
                total_transport (float): Total transport cost.
                total_activities (float): Total activities cost.
            """
            return self.calculator.calculate_total(float(total_accommodation), float(total_food), float(total_transport), float(total_activities))
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate average daily budget.
            Args:
                total_cost (float): Total estimated cost of the trip.
                days (int): Duration of the trip in days.
            """
            return self.calculator.calculate_daily_budget(float(total_cost), int(days))
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]