import numpy as np
import pandas as pd
import phonenumbers
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Categorical, PhoneNumber


class PhoneNumberToArea(TransformPrimitive):
    """Determines the area code of a phone number.

    Description:
        Given a list of phone numbers, return the area code of each
        one. If a phone number is missing or invalid, return np.nan.
        Uses the phonenumbers python library.

    Examples:
        >>> phone_number_to_area = PhoneNumberToArea()
        >>> phone_number_to_area(['+55 55 5555 5555', '+81 75 555 5555', '+1-541-754-3010']).tolist()
        ['55', '75', '541']
    """

    name = "phone_number_to_area"
    input_types = [ColumnSchema(logical_type=PhoneNumber)]
    return_type = ColumnSchema(logical_type=Categorical, semantic_tags={"category"})

    def get_function(self):
        def phone_number_to_area_single(x):
            if pd.isnull(x):
                return np.nan
            try:
                # parse phone number
                pn = phonenumbers.parse(x, None)
                # determine length of area code
                area_code_len = phonenumbers.length_of_geographical_area_code(pn)
                # slice national number for area code
                return str(pn.national_number)[:area_code_len]
            except phonenumbers.phonenumberutil.NumberParseException:
                return np.nan

        def phone_number_to_area(x):
            return x.apply(phone_number_to_area_single)

        return phone_number_to_area
