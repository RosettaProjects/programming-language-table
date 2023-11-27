class Illustration:
    """
    Atomic element, containing a single code illustration with optional annotation. Also requires
      the language code, group id number, and feature id number.
    """

    text: str
    code: str
    lang: str
    group_id: int
    feature_id: int
    ...
