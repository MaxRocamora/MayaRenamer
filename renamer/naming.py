"""Pure naming helpers (no Maya / Qt dependencies)."""

UNDERSCORE = '_'


def is_number(text: str) -> bool:
    """True if the text is an integer (Maya names cannot be numbers only)."""
    try:
        int(text)
    except ValueError:
        return False
    return True


def parse_int(text: str, default: int, minimum: int = None) -> int:
    """Parse text as int, falling back to default when invalid or below minimum."""
    try:
        value = int(text)
    except ValueError:
        return default
    if minimum is not None and value < minimum:
        return default
    return value


def short_name(node: str) -> str:
    """Last element of a DAG path ('|grp|geo' -> 'geo')."""
    return node.rsplit('|', 1)[-1]


def remove_first(name: str, amount: int) -> str:
    """Remove `amount` leading characters, keeping at least one character."""
    if amount > 0 and len(name) > amount:
        return name[amount:]
    return name


def remove_last(name: str, amount: int) -> str:
    """Remove `amount` trailing characters, keeping at least one character."""
    if amount > 0 and len(name) > amount:
        return name[:-amount]
    return name


def add_prefix(name: str, prefix: str) -> str:
    """Prefix the name; empty or numeric prefixes are ignored (invalid in Maya)."""
    if not prefix or is_number(prefix):
        return name
    return prefix + UNDERSCORE + name


def add_suffix(name: str, suffix: str) -> str:
    """Suffix the name; empty suffix is ignored."""
    if not suffix:
        return name
    return name + UNDERSCORE + suffix


def add_padding(name: str, number: int, zeros: int) -> str:
    """Append '_<number>' zero-filled to `zeros` digits."""
    return name + UNDERSCORE + str(number).zfill(zeros)
