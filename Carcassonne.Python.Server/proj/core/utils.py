def nextItem(items: list, index:int) -> any:
    return items[(index + 1) % len(items)]

def prevItem(items: list, index:int) -> any:
    return items[(index - 1) % len(items)]

def indexOf(items: list, predicate: callable) -> int | None:
    return next(
        (index for index, item in enumerate(items) if predicate(item)),
        None
    )

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)

def encodeBase62(value: int) -> str:
    if value == 0:
        return ALPHABET[0]

    chars = []
    while value > 0:
        value, rem = divmod(value, BASE)
        chars.append(ALPHABET[rem])

    return ''.join(reversed(chars))

def decodeBase62(value: str) -> int:
    num = 0

    for char in value:
        num = num * BASE + ALPHABET.index(char)
        
    return num