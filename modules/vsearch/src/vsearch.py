
def vsearch(phrase: str, letter: str = 'aeiou') -> str:
    """Returns a string with the 'letters' found in the 'phrase'."""
    return set(letter).intersection(set(phrase))
