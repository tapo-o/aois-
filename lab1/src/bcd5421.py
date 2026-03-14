def encode_digit_5421(digit: int) -> list[int]:
    """Превращает цифру в список из 4 бит (кодировка 5421 BCD)."""
    bits = [0, 0, 0, 0]
    
    if digit >= 5:
        bits[0] = 1
        remainder = digit - 5
    else:
        bits[0] = 0
        remainder = digit
    
    if remainder >= 4:
        bits[1] = 1
        remainder -= 4
    if remainder >= 2:
        bits[2] = 1
        remainder -= 2
    if remainder >= 1:
        bits[3] = 1
        
    return bits

def decode_digit_5421(bits: list[int]) -> int:
    """Превращает список из 4 бит обратно в десятичную цифру."""
    weights = [5, 4, 2, 1]
    return sum(weights[i] for i in range(4) if bits[i] == 1)

def number_to_bcd_array(number: int) -> list[list[int]]:
    """Превращает число в список списков (массив нибблов)."""
    return [encode_digit_5421(int(d)) for d in str(number)]

def add_bcd_5421(bcdArray1, bcdArray2):
    # 1. Выравниваем массивы по длине, добавляя пустые нибблы [0,0,0,0] в начало
    maxLength = max(len(bcdArray1), len(bcdArray2))
    arr1 = [[0,0,0,0]] * (maxLength - len(bcdArray1)) + bcdArray1
    arr2 = [[0,0,0,0]] * (maxLength - len(bcdArray2)) + bcdArray2
    
    result = []
    carry = 0
    
    # 2. Складываем поразрядно, начиная с конца (младшего разряда)
    for i in range(maxLength - 1, -1, -1):
        digit1 = decode_digit_5421(arr1[i])
        digit2 = decode_digit_5421(arr2[i])
        
        # Суммируем цифры и перенос от предыдущего разряда
        currentSum = digit1 + digit2 + carry
        
        if currentSum >= 10:
            currentSum -= 10
            carry = 1
        else:
            carry = 0
            
        # Кодируем полученную цифру обратно в 5421 и добавляем в начало результата
        result.insert(0, encode_digit_5421(currentSum))
    
    # 3. Если после всех сложений остался перенос — добавляем единицу в начало
    if carry == 1:
        result.insert(0, encode_digit_5421(1))
        
    return result