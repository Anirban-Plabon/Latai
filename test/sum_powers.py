# 1. Define the sequence starting at 1, multiplying by 2 until 1024.
# Note: The prompt asks for 1, 4, 8, 16... implying the sequence 2^n starting from 2^0,
# but skipping 2^1 (which is 2). If the sequence is 1, 2, 4, 8... up to 1024,
# that would be powers of 2. Following the pattern 1, 4, 8, 16...:
# 1 is 2^0, 4 is 2^2, 8 is 2^3, 16 is 2^4, etc.

def generate_custom_sequence(limit):
    # Starting at 1
    yield 1
    # Then continuing with powers of 2 starting from 2^2 (4) up to 1024
    current = 4
    while current <= limit:
        yield current
        current *= 2

# 2. Store the sequence in a variable
sequence = list(generate_custom_sequence(1024))

# 3. Calculate the sum of the sequence
total_sum = sum(sequence)

# 4. Print the resulting sum
print(f"Sequence: {sequence}")
print(f"Sum: {total_sum}")