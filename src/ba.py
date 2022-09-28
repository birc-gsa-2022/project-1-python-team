"""Module for computing border arrays."""


def border_array(x: str) -> list[int]:
    """
    Construct the border array for x.

    >>> border_array("aaba")
    [0, 1, 0, 1]
    >>> border_array("ississippi")
    [0, 0, 0, 1, 2, 3, 4, 0, 0, 1]
    >>> border_array("")
    []
    """

    ba: list[int] = [0]
    stop = len(x)
    i, j = 0, 1
    while i < stop and j < stop:
        if x[i] == x[j]:
            ba.append(ba[j-1] + 1)
            i += 1
            j += 1
        elif x[i] != x[j]:
            ba.append(0)
            i = ba[j]
            j += 1

    return ba  # FIXME


def strict_border_array(x: str) -> list[int]:
    """
    Construct the strict border array for x.

    A strict border array is one where the border cannot
    match on the next character. If b is the length of the
    longest border for x[:i+1], it means x[:b] == x[i-b:i+1],
    but for a strict border, it must be the longest border
    such that x[b] != x[i+1].

    >>> strict_border_array("aaba")
    [0, 1, 0, 1]
    >>> strict_border_array("aaaba")
    [0, 0, 2, 0, 1]
    >>> strict_border_array("ississippi")
    [0, 0, 0, 0, 0, 0, 4, 0, 0, 1]
    >>> strict_border_array("")
    []
    """

    ba = border_array(x)
    bax = []
    end = len(ba)
    for i, b in enumerate(ba):
        if b == 0:
            bax.append(0)
        elif b != 0:
            if i+1 == end:
                bax.append(b)
            elif ba[i+1] != 0:
                bax.append(0)
            else:
                bax.append(b)
    return bax  # FIXME

# Mailunds implementation:


def mailund_border_array(x: str) -> list[int]:

    ba = [0] * len(x)
    for j in range(1, len(x)):
        b = ba[j - 1]
        while b > 0 and x[j] != x[b]:
            b = ba[b - 1]
        ba[j] = b + 1 if x[j] == x[b] else 0
    return ba


def main() -> None:
    print(border_array("ississippi"))
    print(strict_border_array("ississippi"))


if __name__ == "__main__":
    main()
