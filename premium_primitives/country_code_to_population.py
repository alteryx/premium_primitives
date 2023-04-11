import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import CountryCode

from premium_primitives.utils import PremiumDataMixin


class CountryCodeToPopulation(PremiumDataMixin, TransformPrimitive):
    """Determines the population of a country from a country code.

    Description:
        Given a list of country codes, determine the
        population of each one. Accepts `ISO-3166alpha2`,
        `ISO-3166alpha3`, or `ISO-3166numeric` codes.

        If a code is missing or invalid, return `NaN`.

        Population by Country Code were sourced from data
        here: https://www.geonames.org/countries/

    Examples:
        >>> country_code_to_population = CountryCodeToPopulation()
        >>> country_code_to_population(['AM', 'SOM', 780]).tolist()
        [2968000, 10112453, 1328019]
    """

    name = "country_code_to_population"
    input_types = [ColumnSchema(logical_type=CountryCode)]
    return_type = ColumnSchema(semantic_tags={"numeric"})
    default_value = None
    filename = "country_to_continent.csv"

    def get_function(self):
        file_path = self.get_filepath(self.filename)
        data = pd.read_csv(file_path, keep_default_na=False)
        data["Population"] = data["Population"].str.replace(",", "").astype(int)
        country_code_types = ["ISO-3166alpha2", "ISO-3166alpha3", "ISO-3166numeric"]
        continent_by_country_code = data.melt(
            id_vars=["Population"],
            value_vars=country_code_types,
            value_name="country_code",
        )

        def country_code_to_population(x):
            df = pd.DataFrame({"country_code": x})
            df = pd.merge(
                df,
                continent_by_country_code,
                on="country_code",
                how="left",
            )
            return df.Population

        return country_code_to_population
