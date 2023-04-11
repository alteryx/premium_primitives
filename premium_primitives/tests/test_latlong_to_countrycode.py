import numpy as np
import pandas as pd

from premium_primitives.latlong_to_countrycode import LatLongToCountryCode
from premium_primitives.tests.utils import (
    BaseTestTransform,
    find_applicable_primitives,
    valid_dfs,
)


class TestLatLongToCountryCode(BaseTestTransform):
    primitive = LatLongToCountryCode

    def test_latlongs(self):
        primitive_instance = self.primitive()
        primitive_func = primitive_instance.get_function()
        array = pd.Series([(51.52, -0.17), (9.93, 76.25), (37.38, -122.08)])
        answer = pd.Series(["GB", "IN", "US"])
        pd.testing.assert_series_equal(
            primitive_func(array),
            answer,
            check_names=False,
        )

    def test_latlongs_vectorize(self):
        primitive_instance = self.primitive(no_nans=True)
        primitive_func = primitive_instance.get_function()
        array = pd.Series([(51.52, -0.17), (9.93, 76.25), (37.38, -122.08)])
        answer = pd.Series(["GB", "IN", "US"])
        pd.testing.assert_series_equal(
            primitive_func(array),
            answer,
            check_names=False,
        )

    def test_nans(self):
        primitive_instance = self.primitive()
        primitive_func = primitive_instance.get_function()
        array = pd.Series([(np.nan, np.nan), (np.nan, 1), (1, np.nan)])
        answer = pd.Series([None, None, None])
        pd.testing.assert_series_equal(
            primitive_func(array),
            answer,
            check_names=False,
        )

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
