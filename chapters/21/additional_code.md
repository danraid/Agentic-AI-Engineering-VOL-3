# Additional illustrative Python fragments

## Fragment 1

```python
from itertools import product


def allowed(consent, draft_version, current_version, recipient):
    """Toy policy; reject malformed inputs as well as unsafe cases."""
    if type(consent) is not bool:
        return False
    if type(draft_version) is not int or type(current_version) is not int:
        return False
    if recipient not in ("owner", "other"):
        return False
    return (
        consent
        and draft_version == current_version
        and recipient == "owner"
    )


def mutant(consent, draft_version, current_version, recipient):
    """Deliberately defective policy: it omits consent."""
    return draft_version == current_version and recipient == "owner"


def main():
    states = list(product(
        (False, True),  # consent
        (0, 1),         # draft version
        (0, 1),         # current version
        ("owner", "other"),
    ))

    accepted = [s for s in states if allowed(*s)]
    unsafe_mutant = [s for s in states if mutant(*s) and not allowed(*s)]

    # Check both safety and a permitted path in this finite domain.
    assert len(states) == 16
    assert len(accepted) == 2
    assert all(c and d == v and r == "owner" for c, d, v, r in accepted)
    assert allowed(True, 0, 0, "owner")
    assert not allowed(False, 0, 0, "owner")
    assert not allowed(True, 0, 1, "owner")
    assert not allowed(True, 0, 0, "other")

    # Python booleans are integer subclasses; exact type checks matter here.
    assert not allowed(True, True, 1, "owner")
    assert not allowed("yes", 0, 0, "owner")
    assert len(unsafe_mutant) == 2

    print("States:", len(states))
    print("Policy accepts:", len(accepted))
    print("Unsafe mutant accepts:", len(unsafe_mutant))
    for state in unsafe_mutant:
        print("Counterexample:", state)


if __name__ == "__main__":
    main()
```
