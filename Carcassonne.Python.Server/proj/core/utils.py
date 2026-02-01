def nextItem(items: list, index:int) -> any:
    return items[(index + 1) % len(items)]

def prevItem(items: list, index:int) -> any:
    return items[(index - 1) % len(items)]

def indexOf(items: list, predicate: callable) -> int | None:
    return next(
        (index for index, item in enumerate(items) if predicate(item)),
        None
    )