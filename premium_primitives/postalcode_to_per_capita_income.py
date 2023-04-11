import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, PostalCode

from premium_primitives.utils import PremiumDataMixin


class PostalCodeToPerCapitaIncome(PremiumDataMixin, TransformPrimitive):
    """Determines the median per capita income of a Postal Code.

    Description:
        Given a PostalCode, return the median per capita income of that area.
        PostalCodes can be 5-digit or 9-digit. In the case of 9-digit PostalCodes,
        only the first 5 digits are used and any digits after the first five
        are discarded. Return nan if the PostalCode is not found.

        Uses the per capita income in the past 12 months (in 2017
        Inflation-adjusted dollars).

    Examples:
        >>> postalcode_to_per_capita_income = PostalCodeToPerCapitaIncome()
        >>> postalcode_to_per_capita_income(["10001", "82838", "02116-5421"]).tolist()
        [86014.0, 36985.0, 96844.0]
    """

    name = "postalcode_to_per_capita_income"
    input_types = [ColumnSchema(logical_type=PostalCode)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})

    filename = "postalcode_to_per_capita_income_data.csv"

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
