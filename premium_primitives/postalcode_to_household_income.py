import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, PostalCode

from premium_primitives.utils import PremiumDataMixin


class PostalCodeToHouseholdIncome(PremiumDataMixin, TransformPrimitive):
    """Determines the median household income for a Postal Code.

    Description:
        Supports 5 digit PostalCodes, as well as 9 digit PostalCodes
        (will take the first 5 digits in this case).

        Uses the median household income in the past 12 months (in
        2017 inflation-adjusted dollars).

        If PostalCode is not found, return `NaN`.

    Examples:
        >>> postalcode_to_household_income = PostalCodeToHouseholdIncome()
        >>> postalcode_to_household_income(["82838", "02116", "02116-3899"]).tolist()
        [59000.0, 103422.0, 103422.0]
    """

    name = "postalcode_to_household_income"
    input_types = [ColumnSchema(logical_type=PostalCode)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})
    filename = "postalcode_to_household_income_data.csv"

    def get_function(self):
        file_path = self.get_filepath(self.filename)
        data = pd.read_csv(
            file_path,
            names=["postalcode", "income"],
            dtype={"postalcode": str},
        )

        def apply_postalcode_income(col):
            codes = pd.DataFrame({"postalcode": col})
            codes["postalcode"] = (
                codes["postalcode"].astype(str).str.strip().str.slice(0, 5)
            )
            return codes.merge(data, how="left")["income"].values

        return apply_postalcode_income
