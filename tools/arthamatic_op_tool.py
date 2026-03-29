import os
from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

@tool
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.
    Args:
        a (float): The first number.
        b (float): The second number.
    Returns:
        float: The product of a and b.
    """
    return float(a) * float(b)

@tool
def add(a: float, b: float) -> float:
    """
    Add two numbers.
    Args:
        a (float): The first number.
        b (float): The second number.
    Returns:
        float: The sum of a and b.
    """
    return float(a) + float(b)

@tool
def currency_converter(from_curr: str, to_curr: str, value: float) -> float:
    """
    Convert currency from one to another.
    Args:
        from_curr (str): The currency index to convert from.
        to_curr (str): The currency index to convert to.
        value (float): The value to convert.
    Returns:
        float: The converted value.
    """
    os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv('ALPHAVANTAGE_API_KEY')
    alpha_vantage = AlphaVantageAPIWrapper()
    response = alpha_vantage._get_exchange_rate(from_curr, to_curr)
    exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
    return float(value) * float(exchange_rate)