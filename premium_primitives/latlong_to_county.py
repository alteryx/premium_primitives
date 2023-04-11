import numpy as np
import pandas as pd
import reverse_geocoder as rg
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import Categorical, LatLong


class LatLongToCounty(TransformPrimitive):
    """Determines Administrative 2 Region (namely US counties and other countries' equivalents) corresponding to given Latitude and Longitude coordinates.

    Description:
        Given a Lat/Long tuple, calculates the corresponding Administrative 2 Region (namely US county and other countries' equivalents).
            Utilizes the third-party python library located at: https://github.com/thampiman/reverse-geocoder.
            The source of the data is GeoNames.

        This uses a parallelised implementation of K-D trees, which has improved performance especially with large inputs.

        For `NaN`s, it fills the values with None.

        For locations in the ocean, it returns one of the closest regions.

        For invalid LatLong's, i.e. outside +-90 and +-180 respectively, it does not throw an error.
            However, behavior is undefined at this point, and it is up to the user to fix the values before using this primitive.

    Args:
        no_nans (bool): If it contains no nans, then the primitive calls a vectorized function.
            Else, the primitive needs to deal with null values before calling the third-party library.
            Defaults to false.

    Examples:
        >>> latlong_to_admin2 = LatLongToCounty()
        >>> latlong_to_admin2([(51.52, -0.17), (9.93, 76.25), (37.38, -122.08), (np.nan, np.nan)]).tolist()
        ['Greater London', 'Ernakulam', 'Santa Clara County', None]

        If we know we have no missing values, we can choose to make it completely vectorized.
        >>> latlong_to_admin2 = LatLongToCounty(no_nans=True)
        >>> latlong_to_admin2([(51.52, -0.17), (9.93, 76.25), (37.38, -122.08)]).tolist()
        ['Greater London', 'Ernakulam', 'Santa Clara County']
    """

    name = "latlong_to_county"
    input_types = [ColumnSchema(logical_type=LatLong)]
    return_type = ColumnSchema(logical_type=Categorical, semantic_tags={"category"})
    default_value = None

    def __init__(self, no_nans=False):
        self.no_nans = no_nans

    def get_function(self):
        def latlong_to_county(column):
            if self.no_nans:
                results = rg.search(column.to_list(), verbose=False)
                results = pd.Series([location["admin2"] for location in results])
                return results

            latlong_df = pd.DataFrame({"latlongs": column})
            latlong_df["is_null"] = latlong_df.apply(
                lambda row: True
                if any(map(lambda x: pd.isna(x), row["latlongs"]))
                else False,
                axis=1,
            )
            latlongs = latlong_df.apply(
                lambda row: (0, 0) if row["is_null"] else row["latlongs"],
                axis=1,
            ).to_list()

            results = rg.search(latlongs, verbose=False)
            latlong_df["results"] = np.array(
                [location["admin2"] for location in results],
            )
            latlong_df["results"] = latlong_df.apply(
                lambda row: None if row["is_null"] else row["results"],
                axis=1,
            )

            return latlong_df["results"]

        return latlong_to_county
