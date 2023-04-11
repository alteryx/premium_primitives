import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Double, SubRegionCode

from premium_primitives.utils import PremiumDataMixin


class SubRegionCodeToPerCapitaIncome(PremiumDataMixin, TransformPrimitive):
    """Determines the per capita income of a US sub-region.

    Description:
        Converts a ISO 3166-2 region code to the per capita
        income for that region. This currently only works for
        United States region codes.

        The per capita income data used for this primitive was
        obtained from the Federal Reserve Bank of St. Louis
        https://fred.stlouisfed.org/release/tables?rid=151&eid=257197

    Examples:
        >>> sub_region_code_to_per_capita_income = SubRegionCodeToPerCapitaIncome()
        >>> subregions = ["US-AL", "US-IA", "US-VT", "US-DC", "US-MI", "US-NY"]
        >>> sub_region_code_to_per_capita_income(subregions).tolist()
        [40805, 47062, 52225, 79989, 46201, 64540]
    """

    name = "sub_region_code_to_per_capita_income"
    input_types = [ColumnSchema(logical_type=SubRegionCode)]
    return_type = ColumnSchema(logical_type=Double, semantic_tags={"numeric"})

    filename = "sub_region_code_to_per_capita_income_data.csv"

    def get_function(self):
        file_path = self.get_filepath(self.filename)
        data = pd.read_csv(file_path)

        def apply_sub_region_code_income(col):
            df = pd.DataFrame({"code": col})
            df["code"] = df["code"].str.strip()
            df = df.merge(data, how="left")
            return df["income"].values

        return apply_sub_region_code_income
