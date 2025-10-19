# ----- Caesar Cipher -----
def caesar_cipher(text, key, mode):
    result = ""
    for char in text:
        if char.isalpha():
            shift = key if mode == "encrypt" else -key
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


# ----- Vigenère Cipher -----
def vigenere_cipher(text, key, mode):
    result = ""
    key = key.lower()
    j = 0
    for i in range(len(text)):
        char = text[i]
        if char.isalpha():
            k = ord(key[j % len(key)]) - 97
            shift = k if mode == "encrypt" else -k
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
            j += 1
        else:
            result += char
    return result


# ----- Rail Fence Cipher -----
def rail_fence(text, key, mode):
    if mode == "encrypt":
        rail = [''] * key
        row, direction = 0, 1
        for char in text:
            rail[row] += char
            if row == 0:
                direction = 1
            elif row == key - 1:
                direction = -1
            row += direction
        return ''.join(rail)
    else:
        pattern = list(range(key)) + list(range(key - 2, 0, -1))
        pattern = (pattern * (len(text) // len(pattern) + 1))[:len(text)]
        rail_lengths = [pattern.count(i) for i in range(key)]
        pos = 0
        rails = []
        for length in rail_lengths:
            rails.append(list(text[pos:pos + length]))
            pos += length
        result = ''
        for p in pattern:
            result += rails[p].pop(0)
        return result


# ----- Playfair Cipher -----
def generate_playfair_matrix(key):
    key = ''.join(dict.fromkeys(key.lower().replace('j', 'i')))
    alphabet = 'abcdefghiklmnopqrstuvwxyz'
    for c in key:
        alphabet = alphabet.replace(c, '')
    matrix = list(key + alphabet)
    return [matrix[i:i + 5] for i in range(0, 25, 5)]


def playfair_process(text):
    text = text.lower().replace('j', 'i').replace(' ', '')
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else 'x'
        if a == b:
            pairs.append((a, 'x'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    return pairs


def playfair_cipher(text, key, mode):
    matrix = generate_playfair_matrix(key)
    pairs = playfair_process(text)
    result = ''
    for a, b in pairs:
        row_a, col_a = [(r, c) for r in range(5) for c in range(5) if matrix[r][c] == a][0]
        row_b, col_b = [(r, c) for r in range(5) for c in range(5) if matrix[r][c] == b][0]
        if row_a == row_b:
            if mode == 'encrypt':
                result += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
            else:
                result += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            if mode == 'encrypt':
                result += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
            else:
                result += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            result += matrix[row_a][col_b] + matrix[row_b][col_a]
    return result
