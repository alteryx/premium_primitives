import numpy as np
import pandas as pd

from premium_primitives.sub_region_code_to_per_capita_income import (
    SubRegionCodeToPerCapitaIncome,
)
from premium_primitives.tests.utils import (
    BaseTestTransform,
    find_applicable_primitives,
    valid_dfs,
)


class TestSubRegionCodeToPerCapitaIncome(BaseTestTransform):
    primitive = SubRegionCodeToPerCapitaIncome

    def test_regular(self):
        primitive_func = self.primitive().get_function()
        codes = pd.Series(
            [
                "US-AL",
                "US-IA",
                "US-VT",
                "US-DC",
                "US-MI",
                "US-NY",
            ],
        )
        correct_answers = [40805, 47062, 52225, 79989, 46201, 64540]
        answers = primitive_func(codes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_with_whitespace(self):
        primitive_func = self.primitive().get_function()
        codes = pd.Series(
            [
                "US-AL ",
                " US-IA",
                " US-VT ",
                "US-DC",
                "US-MI",
                "US-NY   ",
            ],
        )
        correct_answers = [40805, 47062, 52225, 79989, 46201, 64540]
        answers = primitive_func(codes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_with_empty_and_invalid_input(self):
        primitive_func = self.primitive().get_function()
        codes = pd.Series(
            [
                np.nan,
                "",
                "US-VT ",
                "US-DC",
                7,
                "US-YN",
            ],
        )
        correct_answers = [np.nan, np.nan, 52225, 79989, np.nan, np.nan]
        answers = primitive_func(codes)
        np.testing.assert_array_equal(answers, correct_answers)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instantiate = self.primitive
        transform.append(primitive_instantiate)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
