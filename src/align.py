"""A module for translating between alignments and edits sequences."""


def get_edits(p: str, q: str) -> "tuple[str, str, str]":
    """Extract the edit operations from a pairwise alignment.

    Args:
        p (str): The first row in the pairwise alignment.
        q (str): The second row in the pairwise alignment.

    Returns:
        str: The list of edit operations as a string.

    >>> get_edits('ACCACAGT-CATA', 'A-CAGAGTACAAA')
    ('ACCACAGTCATA', 'ACAGAGTACAAA', 'MDMMMMMMIMMMM')

    """
    assert len(p) == len(q)
    # FIXME: do the actual calculations here
    left, right, edits = '', '', ''
    for left_char, right_char in zip(p, q):
        if left_char == '-':
            edits += 'I'
            right += right_char
        elif right_char == '-':
            edits += 'D'
            left += left_char
        else:
            edits += 'M'
            left += left_char
            right += right_char

    return left, right, edits


def local_align(p: str, x: str, i: int, edits: str) -> "tuple[str, str]":
    """Align two sequences from a sequence of edits.

    Args:
        p (str): The read string we have mapped against x
        x (str): The longer string we have mapped against
        i (int): The location where we have an approximative match
        edits (str): The list of edits to apply, given as a string

    Returns:
        tuple[str, str]: The two rows in the pairwise alignment

    >>> local_align("ACCACAGTCATA", "GTACAGAGTACAAA", 2, "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')

    """

    # FIXME: Compute the alignment rows

    left, right = align(p, x[i:], edits)
    return left, right


def align(p: str, q: str, edits: str) -> "tuple[str, str]":
    """Align two sequences from a sequence of edits.

    Args:
        p (str): The first sequence to align.
        q (str): The second sequence to align
        edits (str): The list of edits to apply, given as a string

    Returns:
        tuple[str, str]: The two rows in the pairwise alignment

    >>> align("ACCACAGTCATA", "ACAGAGTACAAA", "MDMMMMMMIMMMM")
    ('ACCACAGT-CATA', 'A-CAGAGTACAAA')

    """
    # FIXME: Compute the alignment rows
    left, right = '', ''
    i, j = 0, 0
    for edit in edits:
        if edit == 'M':
            left += p[i]
            right += q[j]
            i += 1
            j += 1
        elif edit == 'I':
            left += '-'
            right += q[j]
            j += 1
        elif edit == 'D':
            left += p[i]
            right += '-'
            i += 1
    return left, right


def edit_dist(p: str, x: str, i: int, edits: str) -> int:
    """Get the distance between p and the string that starts at x[i:]
    using the edits.

    Args:
        p (str): The read string we have mapped against x
        x (str): The longer string we have mapped against
        i (int): The location where we have an approximative match
        edits (str): The list of edits to apply, given as a string

    Returns:
        int: The distance from p to x[i:?] described by edits

    >>> edit_dist("accaaagta", "cgacaaatgtcca", 2, "MDMMIMMMMIIM")
    5
    """

    # FIXME: Compute the edit distance
    count = 0
    left, right = local_align(p, x, i, edits)
    for left_char, right_char in zip(left, right):
        if left_char != right_char:
            count += 1
    return count
