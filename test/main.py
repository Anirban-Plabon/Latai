import random

# 1. Generate a list of 10 random integers between 1 and 100
random_numbers = [random.randint(1, 100) for _ in range(10)]

# 2. Calculate the sum of these 10 random integers
total_sum = sum(random_numbers)

# 3. Add 500 to the sum, then multiply by 10 and subtract 400
# Calculation: ((total_sum + 500) * 10) - 400
intermediate_sum = total_sum + 500
final_result = (intermediate_sum * 10) - 400

# 4. Print the individual numbers, the sum, and the final result
print(f"Generated numbers: {random_numbers}")
print(f"Sum of numbers: {total_sum}")
print(f"Final result ((sum + 500) * 10 - 400): {final_result}")