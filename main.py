import time

def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = end_time - start_time
    return result, execution_time

def addition(poly_1, poly_2):
    poly_1 = poly_1.zfill(233)
    poly_2 = poly_2.zfill(233)
    result = ''.join(str(int(a) ^ int(b)) for a, b in zip(poly_1, poly_2))
    return result.lstrip('0') or '0'

def binary_division(dividend, divisor):
    dividend = int(dividend, 2)
    divisor = int(divisor, 2)
    quotient = 0
    while dividend >= divisor:
        shift = len(bin(dividend)) - len(bin(divisor))
        dividend ^= (divisor << shift)
        quotient ^= (1 << shift)
    remainder = bin(dividend)[2:]
    return remainder.zfill(233) or '0'

def multiply_polynomials(poly_1, poly_2, mod_poly):
    poly_1 = poly_1.zfill(233)
    poly_2 = poly_2.zfill(233)
    result = [0] * (2 * 233)
    for i in range(233):
        if poly_2[232 - i] == '1':
            for j in range(233):
                result[i + j] ^= int(poly_1[232 - j])
    result = ''.join(map(str, result))
    return binary_division(result, mod_poly)

def square(poly_1, mod_poly):
    interleaved = ''.join(bit + '0' for bit in poly_1[:-1]) + poly_1[-1]
    return binary_division(interleaved, mod_poly)

def power_poly(poly_1, poly_3, mod_poly):
    result = '1'.zfill(233)
    for bit in poly_3:
        if bit == '1':
            result = multiply_polynomials(result, poly_1, mod_poly)
        poly_1 = square(poly_1, mod_poly)
    return result

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        q, r = divmod(a, b)
        gcd, x1, y1 = extended_gcd(b, r)
        x = y1
        y = x1 - q * y1
        return gcd, x, y

def reverse(poly_1, mod_poly):
    poly_int = int(poly_1, 2)
    mod_int = int(mod_poly, 2)
    gcd, inv, _ = extended_gcd(mod_int, poly_int)
    if gcd != 1:
        raise ValueError("Inverse does not exist")
    inv_bin = bin(inv)[2:]
    return inv_bin.zfill(233) or '0'

def trace(poly):
    return str(sum(map(int, poly)) % 2)

mod = '10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100101001000000000000001'

poly1 = str(input("Enter the first polynomial: "))
poly2 = str(input("Enter the second polynomial: "))
poly3 = str(input("Enter the third polynomial: "))

add_result, add_time = measure_time(addition, poly1, poly2)
print(f'Addition:  {add_result}')
print(f'Time taken for Addition: {add_time} seconds')

mul_result, mul_time = measure_time(multiply_polynomials, poly1, poly2, mod)
print(f'Multiply:  {mul_result}')
print(f'Time taken for Multiply: {mul_time} seconds')

sq_result, sq_time = measure_time(square, poly1, mod)
print(f'Square:  {sq_result}')
print(f'Time taken for Square: {sq_time} seconds')

try:
    reverse_result, reverse_time = measure_time(reverse, poly1, mod)
    print(f'Reverse:  {reverse_result}')
    print(f'Time taken for Reverse: {reverse_time} seconds')
except ValueError as e:
    print(e)

pow_result, pow_time = measure_time(power_poly, poly1, poly3, mod)
print(f'Power:  {pow_result}')
print(f'Time taken for Power: {pow_time} seconds')
