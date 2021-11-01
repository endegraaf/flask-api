import dataclasses


@dataclasses.dataclass(init=False)
class Employee:
    """Employee dataclass
    Containing Employee details
    """
    id: int = None
    name: str = None
    email: str = None
    phone: str = None
    address: str = None

    def __init__(self, **fields):
        # assure extra fields doesn't raise TypeError
        for key, value in fields.items():
            setattr(self, key, value)

    def all_fields_filled(self) -> bool:
        """if any of the dataclass fields is still None, return False"""
        return not any(getattr(self, field.name) is None
                       for field in dataclasses.fields(self))

    def all_fields_filled(self, *fields_names) -> bool:
        """if any of the dataclass fields is still None, return False"""
        if not len(fields_names):
            fields_names = (field.name for field in dataclasses.fields(self))
        return not any(getattr(self, field) is None for field in fields_names)