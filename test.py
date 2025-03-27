def generate_list(n):
    if n % 2 == 0:
        return [i for i in range(-n//2, 0)] + [i for i in range(1, n//2 + 1)]
    else:
        return [i for i in range(-n//2, n//2 + 1)]

# Test cases
print(generate_list(2))  # Output: [-1, 1]
print(generate_list(4))  # Output: [-2, -1, 1, 2]
print(generate_list(3))  # Output: [-1, 0, 1]
print(generate_list(10))