import math

r = 2
while r < 500:
    is_prime = True
    for i in range(2, int(math.sqrt(r)) + 1):
        if r % i == 0:
            is_prime = False
            break
    if is_prime:
        print(r)
    r += 1