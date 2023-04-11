import numpy as np
import pandas as pd

from premium_primitives.phone_number_to_country import PhoneNumberToCountry
from premium_primitives.tests.utils import (
    BaseTestTransform,
    find_applicable_primitives,
    valid_dfs,
)


class TestPhoneNumberToCountry(BaseTestTransform):
    primitive = PhoneNumberToCountry

    def test_numbers(self):
        primitive_func = self.primitive().get_function()
        numbers = pd.Series(
            [
                "+55 85 5555555",
                "+81 55-555-5555",
                "+1-541-754-3010",
                "+44 55-5555-5555 ",
                "+49-89-636-48018",
            ],
        )
        correct_codes = ["BR", "JP", "US", "GB", "DE"]
        np.testing.assert_array_equal(primitive_func(numbers), correct_codes)

    def test_invalid_numbers(self):
        primitive_func = self.primitive().get_function()
        numbers = pd.Series(
            [
                "754-3010",
                "(541) 754-3010",
                "636-48018",
                "5555555555",
                np.nan,
            ],
        )
        correct_codes = [np.nan] * len(numbers)
        np.testing.assert_array_equal(primitive_func(numbers), correct_codes)

    def test_with_featuretools(self, es):
        transform, aggregation = find_applicable_primitives(self.primitive)
        primitive_instance = self.primitive()
        transform.append(primitive_instance)
        valid_dfs(es, aggregation, transform, self.primitive.name.upper())
