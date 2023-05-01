import inspect

import nltk.data
from importlib.util import find_spec

import featuretools
import pkg_resources
from featuretools.primitives import AggregationPrimitive, TransformPrimitive

from premium_primitives.diversity_score import DiversityScore
from premium_primitives.lsa import LSA
from premium_primitives.mean_characters_per_sentence import MeanCharactersPerSentence
from premium_primitives.number_of_sentences import NumberOfSentences
from premium_primitives.part_of_speech_count import PartOfSpeechCount
from premium_primitives.polarity_score import PolarityScore
from premium_primitives.stopword_count import StopwordCount

from premium_primitives.country_code_to_continent import (
    CountryCodeToContinent,
)
from premium_primitives.country_code_to_income import CountryCodeToIncome
from premium_primitives.country_code_to_population import (
    CountryCodeToPopulation,
)
from premium_primitives.latlong_to_city import LatLongToCity
from premium_primitives.latlong_to_countrycode import LatLongToCountryCode
from premium_primitives.latlong_to_county import LatLongToCounty
from premium_primitives.latlong_to_state import LatLongToState
from premium_primitives.phone_number_to_area import PhoneNumberToArea
from premium_primitives.phone_number_to_country import (
    PhoneNumberToCountry,
)
from premium_primitives.postalcode_to_latlong import PostalCodeToLatLong
from premium_primitives.postalcode_to_per_capita_income import (
    PostalCodeToPerCapitaIncome,
)
from premium_primitives.postalcode_to_state import PostalCodeToState
from premium_primitives.sub_region_code_to_median_household_income import (
    SubRegionCodeToMedianHouseholdIncome,
)
from premium_primitives.sub_region_code_to_per_capita_income import (
    SubRegionCodeToPerCapitaIncome,
)
from premium_primitives.sub_region_code_to_region import (
    SubRegionCodeToRegion,
)
from premium_primitives.version import __version__

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

nltk_data_path = pkg_resources.resource_filename(
    "premium_primitives",
    "data/nltk_data/",
)
nltk.data.path.insert(0, nltk_data_path)


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
