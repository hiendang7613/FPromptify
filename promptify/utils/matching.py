
from typing import Dict, List, Tuple


def _unique(items: List[str]) -> List[str]:
    """Remove duplicates without changing order"""
    seen = set()
    output = []
    for item in items:
        if item not in seen:
            output.append(item)
            seen.add(item)
    return output


def find_substrings(
    text: str,
    substrings: List[str],
    *,
    case_sensitive: bool = False,
    single_match: bool = False,
) -> List[Tuple[int, int]]:
    # remove empty and duplicate strings, and lowercase everything if need be
    substrings = [s for s in substrings if s and len(s) > 0]
    if not case_sensitive:
        text = text.lower()
        substrings = [s.lower() for s in substrings]
    substrings = _unique(substrings)
    offsets = []
    for substring in substrings:
        search_from = 0
        # Search until one hit is found. Continue only if single_match is False.
        while True:
            start = text.find(substring, search_from)
            if start == -1:
                break
            end = start + len(substring)
            offsets.append((start, end))
            if single_match:
                break
            search_from = end
    return offsets


# def test_multiple_substrings():
#     text = "The Blargs is the debut album by rock band The Blargs."
#     substrings = ["The Blargs", "rock"]
#     res = _find_substrings(text, substrings, single_match=False)
#     assert res == [(0, 10), (43, 53), (33, 37)]
#     res = _find_substrings(text, substrings, single_match=True)
#     assert res == [(0, 10), (33, 37)]

# test_multiple_substrings()