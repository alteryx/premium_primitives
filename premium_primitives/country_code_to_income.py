import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import CountryCode

from premium_primitives.utils import PremiumDataMixin


class CountryCodeToIncome(PremiumDataMixin, TransformPrimitive):
    """Transforms a 2-digit or 3-digit ISO-3166-1 country code
    into Gross National Income (GNI) per capita.

    Description:
        The GNI per capita data was obtained from The World Bank
        (https://data.worldbank.org/indicator/NY.GNP.PCAP.CD).
        The GNI data uses 3-digit country codes. In order to use
        2-digit codes, the GNI data was merged with a list of country
        codes obtained from Wikipedia
        (https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).

    Examples:
        >>> country_code_to_income = CountryCodeToIncome()
        >>> country_code_to_income(['USA', 'AM', 'EC']).tolist()
        [58270.0, 3990.0, 5920.0]
    """

    name = "country_code_to_income"
    input_types = [ColumnSchema(logical_type=CountryCode)]
    return_type = ColumnSchema(semantic_tags={"numeric"})
    filename = "GNI_per_capita.csv"

    def get_function(self):
        file_path = self.get_filepath(self.filename)
        income_df = pd.read_csv(file_path)
        income_df["Country Code"] = income_df["Country Code"].str.strip().str.upper()

        def country_code_to_income(x):
            df = pd.DataFrame({"Country Code": x}, dtype=str)
            df["Country Code"] = df["Country Code"].str.strip().str.upper()
            df = df.merge(income_df, how="left")
            return df["2017"].values

        return country_code_to_income
