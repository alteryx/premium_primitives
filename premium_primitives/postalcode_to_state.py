import numpy as np
import zipcodes
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Categorical, PostalCode


class PostalCodeToState(TransformPrimitive):
    """Extracts the state from a PostalCode.

    Description:
        Given a PostalCode, return the state it's in. PostalCodes can be 5-digit or
        9-digit. In the case of 9-digit PostalCodes, only the first 5 digits are
        used and any digits after the first five are discarded. Return nan if
        the PostalCode is not found.

        This primitive uses the ziptools pypi package which only supports
        US PostalCodes at this time.

    Examples:
        >>> postalcode_to_state = PostalCodeToState()
        >>> states = postalcode_to_state(['60622', '94120', '02111-1253'])
        >>> list(map(str, states))
        ['IL', 'CA', 'MA']
    """

    name = "postalcode_to_state"
    input_types = [ColumnSchema(logical_type=PostalCode)]
    return_type = ColumnSchema(logical_type=Categorical, semantic_tags={"category"})

    def get_function(self):
        def postal_to_state(x):
            def postalcode_convert(postalcode):
                try:
                    if not isinstance(postalcode, str):
                        postalcode = str(postalcode)
                    postalcode = postalcode.strip()
                    if len(postalcode) > 5:
                        postalcode = postalcode[:5]
                    state = zipcodes.matching(postalcode)[0]["state"]
                except (ValueError, IndexError, TypeError):
                    state = np.nan
                return state

            return x.apply(postalcode_convert)

        return postal_to_state
