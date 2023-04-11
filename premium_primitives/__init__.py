import inspect

import featuretools
import pkg_resources
from featuretools.primitives import AggregationPrimitive, TransformPrimitive

from premium_primitives.country_code_to_continent import (  # noqa: F401
    CountryCodeToContinent,
)
from premium_primitives.country_code_to_income import CountryCodeToIncome  # noqa: F401
from premium_primitives.country_code_to_population import (  # noqa: F401
    CountryCodeToPopulation,
)
from premium_primitives.latlong_to_city import LatLongToCity  # noqa: F401
from premium_primitives.latlong_to_countrycode import LatLongToCountryCode  # noqa: F401
from premium_primitives.latlong_to_county import LatLongToCounty  # noqa: F401
from premium_primitives.latlong_to_state import LatLongToState  # noqa: F401
from premium_primitives.phone_number_to_area import PhoneNumberToArea  # noqa: F401
from premium_primitives.phone_number_to_country import (  # noqa: F401
    PhoneNumberToCountry,
)
from premium_primitives.postalcode_to_household_income import (  # noqa: F401
    PostalCodeToHouseholdIncome,
)
from premium_primitives.postalcode_to_latlong import PostalCodeToLatLong  # noqa: F401
from premium_primitives.postalcode_to_per_capita_income import (  # noqa: F401
    PostalCodeToPerCapitaIncome,
)
from premium_primitives.postalcode_to_state import PostalCodeToState  # noqa: F401
from premium_primitives.sub_region_code_to_median_household_income import (  # noqa: F401
    SubRegionCodeToMedianHouseholdIncome,
)
from premium_primitives.sub_region_code_to_per_capita_income import (  # noqa: F401
    SubRegionCodeToPerCapitaIncome,
)
from premium_primitives.sub_region_code_to_region import (  # noqa: F401
    SubRegionCodeToRegion,
)
from premium_primitives.version import __version__  # noqa: F401

PREMIUM_PRIMITIVES = [
    obj
    for obj in globals().values()
    if (
        inspect.isclass(obj)
        and obj is not AggregationPrimitive
        and obj is not TransformPrimitive
        and issubclass(obj, (AggregationPrimitive, TransformPrimitive))
    )
]


# set data primitives BEFORE we import them
premium_primitives_data_folder = pkg_resources.resource_filename(
    "premium_primitives",
    "data/",
)
featuretools.config.set(
    {
        "premium_primitives_data_folder": premium_primitives_data_folder,
    },
)
