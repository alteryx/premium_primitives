import numpy as np
import pandas as pd
from featuretools.primitives import Latitude, Longitude
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import LatLong

from premium_primitives.postalcode_to_latlong import PostalCodeToLatLong
from premium_primitives.tests.utils import (
    BaseTestTransform,
    find_applicable_primitives,
    valid_dfs,
)


class TestPostalCodeToLatLong(BaseTestTransform):
    primitive = PostalCodeToLatLong

    def test_postalcode_to_latlong_valid_5digit(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["94120", "00501", "96863"])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(
            [
                (37.7749, -122.4194),
                (40.8154, -73.0451),
                (21.316, -157.8677),
            ],
            name="latlong",
        )
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_latlong_valid_9digit_nodash(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["941201234", "005013512", "968631245"])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(
            [
                (37.7749, -122.4194),
                (40.8154, -73.0451),
                (21.316, -157.8677),
            ],
            name="latlong",
        )
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_latlong_valid_9digit_withdash(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["94120-1234", "00501-3512", "96863-1245"])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(
            [(37.7749, -122.4194), (40.8154, -73.0451), (21.316, -157.8677)],
            name="latlong",
        )
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_latlong_invalid_codes(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["9412", "00501", "968a4", 94120, 968631234, 91234.34])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(
            [
                np.nan,
                (40.8154, -73.0451),
                np.nan,
                (37.7749, -122.4194),
                (21.316, -157.8677),
                np.nan,
            ],
            name="latlong",
        )
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_latlong_integer_input(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([94120, 968631234, 9123])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(
            [(37.7749, -122.4194), (21.316, -157.8677), np.nan],
            name="latlong",
        )
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_latlong_bool_input(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([True, False, "94120"])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(
            [np.nan, np.nan, (37.7749, -122.4194)],
            name="latlong",
        )
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_latlong_nan(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["94120", np.nan, "96863-1245"])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(
            [(37.7749, -122.4194), np.nan, (21.316, -157.8677)],
            name="latlong",
        )
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_latlong_allnan(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([np.nan, np.nan, np.nan])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series([np.nan, np.nan, np.nan], name="latlong", dtype=str)
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        transform.append(Latitude)
        transform.append(Longitude)
        return_types = [ColumnSchema(logical_type=LatLong)]
        valid_dfs(
            es,
            aggregation,
            transform,
            self.primitive.name.upper(),
            return_types=return_types,
        )
