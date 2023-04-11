import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, SubRegionCode

from premium_primitives.utils import PremiumDataMixin


class SubRegionCodeToMedianHouseholdIncome(PremiumDataMixin, TransformPrimitive):
    """Determines the median household income of a US sub-region.

    Description:
        Converts a ISO 3166-2 region code to the median household
        income for that region. This currently only works for
        United States region codes.

        The median income data used for this was obtained from the
        US Census Bureau Table H-8:
        https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html

    Examples:
        >>> sub_region_code_to_median_household_income = SubRegionCodeToMedianHouseholdIncome()
        >>> subregions = ["US-AL", "US-IA", "US-VT", "US-DC", "US-MI", "US-NY"]
        >>> sub_region_code_to_median_household_income(subregions).tolist()
        [51113, 63481, 63805, 83382, 57700, 62447]
    """

    name = "sub_region_code_to_median_household_income"
    input_types = [ColumnSchema(logical_type=SubRegionCode)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})

    filename = "sub_region_code_to_median_household_income_data.csv"

    def get_function(self):
        file_path = self.get_filepath(self.filename)
        data = pd.read_csv(file_path)

        def apply_sub_region_code_income(col):
            df = pd.DataFrame({"code": col})
            df["code"] = df["code"].str.strip()
            df = df.merge(data, how="left")
            return df["income"].values

        return apply_sub_region_code_income
