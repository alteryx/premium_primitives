import numpy as np
import pandas as pd

from premium_primitives.country_code_to_income import CountryCodeToIncome
from premium_primitives.tests.utils import (
    BaseTestTransform,
    find_applicable_primitives,
    valid_dfs,
)


class TestCountryCodeToIncome(BaseTestTransform):
    primitive = CountryCodeToIncome

    def test_country_code_to_income_valid_data(self):
        primitive_func = self.primitive().get_function()
        array = pd.Series(["USA", "AM", "EC", "GBR"])
        answer = pd.Series(primitive_func(array))
        correct_answer = pd.Series([58270.0, 3990.0, 5920.0, 40530.0])
        pd.testing.assert_series_equal(answer, correct_answer)

    def test_country_code_to_income_capitalization(self):
        primitive_func = self.primitive().get_function()
        array = pd.Series(["US", "uS", "Usa", "us", "UsA"])
        answer = pd.Series(primitive_func(array))
        correct_answer = pd.Series([58270.0, 58270.0, 58270.0, 58270.0, 58270.0])
        pd.testing.assert_series_equal(answer, correct_answer)

    def test_country_code_to_income_empty_input(self):
        primitive_func = self.primitive().get_function()
        array = pd.Series([], dtype="string")
        answer = pd.Series(primitive_func(array))
        correct_answer = pd.Series([], dtype="float64")
        pd.testing.assert_series_equal(answer, correct_answer)

    def test_country_code_to_income_nan(self):
        primitive_func = self.primitive().get_function()
        array = pd.Series(["US", np.nan, "EC", "GB"])
        answer = pd.Series(primitive_func(array))
        correct_answer = pd.Series([58270.0, np.nan, 5920.0, 40530.0])
        pd.testing.assert_series_equal(answer, correct_answer)

    def test_country_code_to_income_empty_string(self):
        primitive_func = self.primitive().get_function()
        array = pd.Series(["US", "", "EC", "GB"])
        answer = pd.Series(primitive_func(array))
        correct_answer = pd.Series([58270.0, np.nan, 5920.0, 40530.0])
        pd.testing.assert_series_equal(answer, correct_answer)

    def test_country_code_to_income_spaces(self):
        primitive_func = self.primitive().get_function()
        array = pd.Series(["US", " AM", "EC ", " GB "])
        answer = pd.Series(primitive_func(array))
        correct_answer = pd.Series([58270.0, 3990.0, 5920.0, 40530.0])
        pd.testing.assert_series_equal(answer, correct_answer)

    def test_country_code_to_income_numeric_input(self):
        primitive_func = self.primitive().get_function()
        array = pd.Series(["US", 1234, "EC", 123.34])
        answer = pd.Series(primitive_func(array))
        correct_answer = pd.Series([58270.0, np.nan, 5920.0, np.nan])
        pd.testing.assert_series_equal(answer, correct_answer)

    def test_country_code_to_income_country_with_no_data(self):
        primitive_func = self.primitive().get_function()
        array = pd.Series(["US", "AM", "CU", "GB"])
        answer = pd.Series(primitive_func(array))
        correct_answer = pd.Series([58270.0, 3990.0, np.nan, 40530.0])
        pd.testing.assert_series_equal(answer, correct_answer)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
