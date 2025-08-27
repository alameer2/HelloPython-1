#!/usr/bin/env python3
"""
A basic Python file named 'hello' with fundamental functionality.
This script demonstrates basic Python concepts and operations.
"""

def greet(name="World"):
    """
    A simple greeting function that takes a name and returns a greeting message.
    
    Args:
        name (str): The name to greet. Defaults to "World".
    
    Returns:
        str: A formatted greeting message.
    """
    return f"Hello, {name}!"

def calculate_sum(a, b):
    """
    Calculate the sum of two numbers.
    
    Args:
        a (int/float): First number
        b (int/float): Second number
    
    Returns:
        int/float: Sum of the two numbers
    """
    return a + b

def main():
    """
    Main function demonstrating basic Python functionality.
    """
    # Basic variable assignments
    name = "Python Developer"
    number1 = 10
    number2 = 25
    
    # Print basic greeting
    print("=" * 40)
    print("Welcome to the Hello Python Script!")
    print("=" * 40)
    
    # Demonstrate function usage
    greeting_message = greet(name)
    print(greeting_message)
    
    # Demonstrate arithmetic operations
    result = calculate_sum(number1, number2)
    print(f"The sum of {number1} and {number2} is: {result}")
    
    # Basic list operations
    numbers = [1, 2, 3, 4, 5]
    print(f"Numbers list: {numbers}")
    print(f"Sum of all numbers: {sum(numbers)}")
    print(f"Maximum number: {max(numbers)}")
    print(f"Minimum number: {min(numbers)}")
    
    # Basic string operations
    sample_text = "Hello Python World"
    print(f"Original text: {sample_text}")
    print(f"Uppercase: {sample_text.upper()}")
    print(f"Lowercase: {sample_text.lower()}")
    print(f"Word count: {len(sample_text.split())}")
    
    # Basic loop demonstration
    print("\nCounting from 1 to 5:")
    for i in range(1, 6):
        print(f"Count: {i}")
    
    # Basic conditional logic
    user_number = 42
    if user_number > 50:
        print(f"{user_number} is greater than 50")
    elif user_number == 42:
        print(f"{user_number} is the answer to everything!")
    else:
        print(f"{user_number} is less than 50")
    
    print("\nScript execution completed successfully!")

if __name__ == "__main__":
    main()
