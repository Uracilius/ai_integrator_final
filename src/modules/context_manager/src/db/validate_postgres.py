from dataclasses import fields, is_dataclass
from ....shared.DTO.context_data import ContextDTO
from typing import Any

def validate_context_dto(context_dto: ContextDTO):
    """
    Validates the provided ContextDTO instance to ensure all required fields are present.

    :param context_dto: An instance of ContextDTO.
    :raises ValueError: If any required field is missing.
    """
    if not is_dataclass(context_dto):
        raise ValueError("Provided object is not a dataclass instance.")

    missing_fields = [f.name for f in fields(context_dto) if getattr(context_dto, f.name) is None and f.name != 'id']
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
