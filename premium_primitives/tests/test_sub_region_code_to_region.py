import numpy as np
import pandas as pd

from premium_primitives.sub_region_code_to_region import SubRegionCodeToRegion
from premium_primitives.tests.utils import (
    BaseTestTransform,
    find_applicable_primitives,
    valid_dfs,
)


class TestSubRegionCodeToRegion(BaseTestTransform):
    primitive = SubRegionCodeToRegion

    def test_us_codes(self):
        primitive_func = self.primitive().get_function()
        subregioncodes = pd.Series(
            [
                "US-AZ",
                "US-NY",
                "US-CA",
                "US-TX",
                "US-WI",
            ],
        )
        results = primitive_func(subregioncodes)
        correct_regions = pd.Series(["west", "northeast", "west", "south", "midwest"])
        pd.testing.assert_series_equal(results, correct_regions, check_names=False)

    def test_international_codes(self):
        primitive_func = self.primitive().get_function()
        subregioncodes = pd.Series(
            [
                "UG-219",
                "ZM-06",
                "CA-AB",
            ],
        )
        results = primitive_func(subregioncodes)
        correct_regions = pd.Series([np.nan, np.nan, np.nan], dtype="object")
        pd.testing.assert_series_equal(results, correct_regions, check_names=False)

    def test_nan(self):
        primitive_func = self.primitive().get_function()
        subregioncodes = pd.Series(
            [
                "",
                np.nan,
                "US-AZ",
            ],
        )
        results = primitive_func(subregioncodes)
        correct_regions = pd.Series([np.nan, np.nan, "west"], dtype="object")
        pd.testing.assert_series_equal(results, correct_regions, check_names=False)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
