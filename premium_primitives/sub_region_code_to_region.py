import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import SubRegionCode

from premium_primitives.utils import PremiumDataMixin


class SubRegionCodeToRegion(PremiumDataMixin, TransformPrimitive):
    """Determines the region of a US sub-region.

    Description:
        Converts a ISO 3166-2 region code to a higher-level US
        region. (e.g. US-MA --> northeast, US-CA --> west).

        Possible values include the following:
        `['West', 'South', 'Northeast', 'Midwest']`

        SubRegionCode -> region mappings were sourced from
        this repo:
        https://github.com/cphalpert/census-regions

    Examples:
        >>> sub_region_code_to_region = SubRegionCodeToRegion()
        >>> subregions = ["US-AL", "US-IA", "US-VT", "US-DC", "US-MI", "US-NY"]
        >>> sub_region_code_to_region(subregions).tolist()
        ['south', 'midwest', 'northeast', 'south', 'midwest', 'northeast']
    """

    name = "sub_region_code_to_region"
    input_types = [ColumnSchema(logical_type=SubRegionCode)]
    return_type = ColumnSchema(logical_type=SubRegionCode, semantic_tags={"category"})
    filename = "census_regions.csv"

    def get_function(self):
        file_path = self.get_filepath(self.filename)
        census_data = pd.read_csv(file_path)

        def sub_region_code_to_region(x):
            df = pd.DataFrame({"State Code": x})
            df = pd.merge(df, census_data, how="left")
            return df.Region.str.lower()

        return sub_region_code_to_region
