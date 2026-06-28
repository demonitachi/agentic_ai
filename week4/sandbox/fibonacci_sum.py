def fibonacci_sum(n):
    a, b = 0, 1
    total_sum = 0
    while a < n:
        total_sum += a
        a, b = b, a + b
    return total_sum

result = fibonacci_sum(100)
print(result)