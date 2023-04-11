import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import CountryCode

from premium_primitives.utils import PremiumDataMixin


class CountryCodeToContinent(PremiumDataMixin, TransformPrimitive):
    """Determines the continent from a country code.

    Description:
        Given a list of country codes, determine the
        continent of each one. Accepts `ISO-3166alpha2`,
        `ISO-3166alpha3`, or `ISO-3166numeric` codes.

        If a code is missing or invalid, return `NaN`.

        Continents by Country Code were sourced from data
        here: https://www.geonames.org/countries/

    Examples:
        >>> country_code_to_continent = CountryCodeToContinent()
        >>> country_code_to_continent(['AM', 'SOM', 780]).tolist()
        ['Asia', 'Africa', 'North America']
    """

    name = "country_code_to_continent"
    input_types = [ColumnSchema(logical_type=CountryCode)]
    return_type = ColumnSchema(semantic_tags={"category"})
    default_value = None
    filename = "country_to_continent.csv"

    def get_function(self):
        file_path = self.get_filepath(self.filename)
        data = pd.read_csv(file_path, keep_default_na=False)
        country_code_types = ["ISO-3166alpha2", "ISO-3166alpha3", "ISO-3166numeric"]
        continent_by_country_code = data.melt(
            id_vars=["Continent"],
            value_vars=country_code_types,
            value_name="country_code",
        )

        def country_code_to_continent(x):
            df = pd.DataFrame({"country_code": x})
            df = pd.merge(
                df,
                continent_by_country_code,
                on="country_code",
                how="left",
            )
            return df.Continent

        return country_code_to_continent
