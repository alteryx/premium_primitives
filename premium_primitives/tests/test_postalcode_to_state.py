import numpy as np
import pandas as pd

from premium_primitives.postalcode_to_state import PostalCodeToState
from premium_primitives.tests.utils import (
    BaseTestTransform,
    find_applicable_primitives,
    valid_dfs,
)


class TestPostalCodeToState(BaseTestTransform):
    primitive = PostalCodeToState

    def test_postalcode_to_state_valid_5digit(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["60622", "94120", "02111"])
        answers = primitive_func(postalcodes)
        correct_answers = ["IL", "CA", "MA"]
        np.testing.assert_array_equal(answers, correct_answers)

    def test_postalcode_to_state_valid_9digit_nodash(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["606221234", "941202341", "021111253"])
        answers = primitive_func(postalcodes)
        correct_answers = ["IL", "CA", "MA"]
        np.testing.assert_array_equal(answers, correct_answers)

    def test_postalcode_to_state_valid_9digit_withdash(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["60622-1234", "94120-2341", "02111-1253"])
        answers = primitive_func(postalcodes)
        correct_answers = ["IL", "CA", "MA"]
        np.testing.assert_array_equal(answers, correct_answers)

    def test_postalcode_to_state_valid_with_whitespace(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([" 60622", "94120 ", " 02111 "])
        answers = primitive_func(postalcodes)
        correct_answers = ["IL", "CA", "MA"]
        np.testing.assert_array_equal(answers, correct_answers)

    def test_postalcode_to_state_with_nan(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["60622", "94120", np.nan])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(["IL", "CA", np.nan])
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_state_all_nan(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([np.nan, np.nan, np.nan])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series([np.nan, np.nan, np.nan])
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_state_with_invalid_codes(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["60622", "6062", "abc"])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(["IL", np.nan, np.nan])
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_state_integer_input(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([60622, 94120, 2111])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series(["IL", "CA", np.nan])
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_postalcode_to_state_bool_input(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([True, False, "02111"])
        answers = primitive_func(postalcodes)
        correct_answers = pd.Series([np.nan, np.nan, "MA"])
        pd.testing.assert_series_equal(answers, correct_answers)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
