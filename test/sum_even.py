# Initialize a variable total to 0
total = 0

# Create a loop that iterates through numbers from 1 to 100
for number in range(1, 101):
    # Use a conditional statement to check if the number is even
    if number % 2 == 0:
        # Add the number to total if it is even
        total += number

# Print the final result
print(f"The sum of all even numbers from 1 to 100 is: {total}")