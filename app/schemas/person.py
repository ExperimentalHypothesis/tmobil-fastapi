from typing import Any
from pydantic import BaseModel, validator
from datetime import datetime
import re

VALID_DATE_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"

class Person(BaseModel):
    """ Base class to be subclassed by CustomerReq class """
    first_name: str = None
    last_name: str = None
    dob: str = None

    @validator("dob", pre=True)
    def validate_dob_format(cls, value: Any) -> Any:
        if re.match(VALID_DATE_PATTERN, value):
            return value
        raise ValueError("Invalid date format. Use YYYY-MM-DD")

