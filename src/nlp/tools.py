from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """
    print(f"Adding {a} and {b}")
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """
    print(f"Multiplying {a} and {b}")
    return a * b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two integers.

    Args:
        a: First integer
        b: Second integer
    """
    print(f"Subtracting {b} from {a}")
    return a - b

tools = [add, multiply, subtract]