import numpy as np
import pandas as pd

from premium_primitives.postalcode_to_per_capita_income import (
    PostalCodeToPerCapitaIncome,
)
from premium_primitives.tests.utils import (
    BaseTestTransform,
    find_applicable_primitives,
    valid_dfs,
)


class TestPostalCodeToPerCapitaIncome(BaseTestTransform):
    primitive = PostalCodeToPerCapitaIncome

    def test_valid_5digit(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["10001", "82838", "02116"])
        correct_answers = [86014, 36985, 96844]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_valid_9digit_nodash(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["100011234", "828384531", "021165421"])
        correct_answers = [86014, 36985, 96844]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_valid_9digit_withdash(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["10001-1234", "82838-4531", "02116-5421"])
        correct_answers = [86014, 36985, 96844]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_with_whitespace(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([" 10001", "82838 ", " 02116 "])
        correct_answers = [86014, 36985, 96844]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_nan(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["10001", np.nan, "02116"])
        correct_answers = [86014, np.nan, 96844]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_all_nan(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([np.nan, np.nan, np.nan])
        correct_answers = [np.nan, np.nan, np.nan]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_invalid_codes(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series(["1234567890", "00000"])
        correct_answers = [np.nan, np.nan]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_integer_input(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([10001, 82838])
        correct_answers = [86014, 36985]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_bool_input(self):
        primitive_func = self.primitive().get_function()
        postalcodes = pd.Series([True, False, "02116"])
        correct_answers = [np.nan, np.nan, 96844]
        answers = primitive_func(postalcodes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instantiate = self.primitive
        transform.append(primitive_instantiate)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
