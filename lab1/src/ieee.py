def ieee_to_float(binary_array: list[int]) -> float:
    if len(binary_array) != 32:
        raise ValueError("Массив должен содержать ровно 32 бита")

    sign = binary_array[0]
    exp_bits = binary_array[1:9]
    frac_bits = binary_array[9:32]
    
    exponent = sum(bit * (2 ** i) for i, bit in enumerate(reversed(exp_bits)))
    fraction = sum(bit * (2 ** -(i + 1)) for i, bit in enumerate(frac_bits))
        
    if exponent == 0 and fraction == 0:
        return -0.0 if sign == 1 else 0.0
        
    value = (1.0 + fraction) * (2 ** (exponent - 127))
    return -value if sign == 1 else value

def float_to_ieee(value: float) -> list[int]:
    if value == 0.0:
        is_negative_zero = str(value).startswith('-')
        return [1 if is_negative_zero else 0] + [0] * 31
        
    sign = 1 if value < 0 else 0
    abs_val = abs(value)
    
    exponent = 0
    if abs_val >= 1.0:
        while abs_val >= 2.0:
            abs_val /= 2.0
            exponent += 1
    else:
        while abs_val < 1.0:
            abs_val *= 2.0
            exponent -= 1
            
    biased_exp = exponent + 127
    exp_array = []
    for _ in range(8):
        exp_array.insert(0, biased_exp % 2)
        biased_exp //= 2
        
    fraction = abs_val - 1.0
    mantissa_array = []
    for _ in range(23):
        fraction *= 2.0
        if fraction >= 1.0:
            mantissa_array.append(1)
            fraction -= 1.0
        else:
            mantissa_array.append(0)
            
    return [sign] + exp_array + mantissa_array

def unpack_parts(ieee_array: list[int]) -> tuple[int, int, int]:
    sign = ieee_array[0]
    
    exponent = 0
    for bit in ieee_array[1:9]:
        exponent = (exponent << 1) | bit
        
    fraction = 0
    for bit in ieee_array[9:32]:
        fraction = (fraction << 1) | bit
    
    mantissa = (1 << 23) | fraction if exponent > 0 else 0
    return sign, exponent, mantissa

def pack_parts(sign: int, exponent: int, mantissa: int) -> list[int]:
    fraction_value = mantissa & ((1 << 23) - 1)
    exp_bits = [(exponent >> i) & 1 for i in range(7, -1, -1)]
    frac_bits = [(fraction_value >> i) & 1 for i in range(22, -1, -1)]
        
    return [sign] + exp_bits + frac_bits

# Оставил логику математических операций как есть, обновив только вызовы функций
def multiply_ieee(arr1: list[int], arr2: list[int]) -> list[int]:
    s1, e1, m1 = unpack_parts(arr1)
    s2, e2, m2 = unpack_parts(arr2)
    
    if m1 == 0 or m2 == 0: 
        return [0] * 32
    
    res_sign = s1 ^ s2
    res_exp = e1 + e2 - 127
    res_mant = m1 * m2
    
    if res_mant & (1 << 47):
        res_mant >>= 24
        res_exp += 1
    else:
        res_mant >>= 23
        
    return pack_parts(res_sign, res_exp, res_mant)

def divide_ieee(arr1: list[int], arr2: list[int]) -> list[int]:
    s1, e1, m1 = unpack_parts(arr1)
    s2, e2, m2 = unpack_parts(arr2)
    
    if m2 == 0: 
        raise ZeroDivisionError("Division by zero")
    if m1 == 0: 
        return [0] * 32
    
    res_sign = s1 ^ s2
    res_exp = e1 - e2 + 127
    res_mant = (m1 << 23) // m2
    
    if not (res_mant & (1 << 23)):
        res_mant <<= 1
        res_exp -= 1
        
    return pack_parts(res_sign, res_exp, res_mant)

def add_ieee(arr1: list[int], arr2: list[int]) -> list[int]:
    s1, e1, m1 = unpack_parts(arr1)
    s2, e2, m2 = unpack_parts(arr2)
    
    if m1 == 0: return arr2
    if m2 == 0: return arr1
    
    if e2 > e1:
        s1, s2, e1, e2, m1, m2 = s2, s1, e2, e1, m2, m1
        
    diff = e1 - e2
    if diff > 24:
        m2 = 0
    else:
        m2 >>= diff
        
    res_exp = e1
    
    if s1 == s2:
        res_sign = s1
        res_mant = m1 + m2
    else:
        if m1 >= m2:
            res_sign = s1
            res_mant = m1 - m2
        else:
            res_sign = s2
            res_mant = m2 - m1
            
    if res_mant == 0: 
        return [0] * 32
    
    if res_mant & (1 << 24):
        res_mant >>= 1
        res_exp += 1
    else:
        while not (res_mant & (1 << 23)) and res_exp > 0:
            res_mant <<= 1
            res_exp -= 1
            
    return pack_parts(res_sign, res_exp, res_mant)

def sub_ieee(arr1: list[int], arr2: list[int]) -> list[int]:
    arr2_inverted = arr2[:]
    arr2_inverted[0] = 1 - arr2_inverted[0]
    return add_ieee(arr1, arr2_inverted)