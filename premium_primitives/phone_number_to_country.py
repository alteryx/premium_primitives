import numpy as np
import pandas as pd
import phonenumbers
from featuretools.primitives.base import TransformPrimitive
from phone_iso3166.country import phone_country
from phone_iso3166.errors import InvalidPhone
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Categorical, PhoneNumber


class PhoneNumberToCountry(TransformPrimitive):
    """Determines the country of a phone number.

    Description:
        Given a list of phone numbers, return the country of each
        one, based on the country code. If a phone number is missing
        or invalid, return np.nan. Uses the phonenumbers and phone_iso3166
        python libraries.

    Examples:
        >>> phone_number_to_country = PhoneNumberToCountry()
        >>> phone_number_to_country(['+55 85 5555555', '+81 55-555-5555', '+1-541-754-3010',]).tolist()
        ['BR', 'JP', 'US']
    """

    name = "phone_number_to_country"
    input_types = [ColumnSchema(logical_type=PhoneNumber)]
    return_type = ColumnSchema(logical_type=Categorical, semantic_tags={"category"})

    def get_function(self):
        def phone_number_to_country_single(x):
            if pd.isnull(x):
                return np.nan
            # parse phone number
            try:
                pn = phonenumbers.parse(x, None)
                pn = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.phonenumberutil.NumberParseException:
                return np.nan

            # look up country code
            try:
                return phone_country(pn)
            except InvalidPhone:
                return np.nan

        def phone_number_to_country(x):
            return x.apply(phone_number_to_country_single)

        return phone_number_to_country
