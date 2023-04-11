import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import LatLong, PostalCode

from premium_primitives.utils import PremiumDataMixin


class PostalCodeToLatLong(PremiumDataMixin, TransformPrimitive):
    """Determines the Latitude and Longitude coordinates of a Postal Code.

    Description:
        Given a PostalCode, return its Latitude and Longitude coordinates as a tuple.
        PostalCodes can be 5-digit or 9-digit. In the case of 9-digit PostalCodes,
        only the first 5 digits are used and any digits after the first five
        are discarded. Return nan if the PostalCode is not found.

        The data for this transform was obtained from www.geonames.org.
        (http://download.geonames.org/export/zip/allCountries.zip)

    Examples:
        >>> postalcode_to_latlong = PostalCodeToLatLong()
        >>> postalcode_to_latlong(['94120', '00501', '96863-1245']).to_list()
        [(37.7749, -122.4194), (40.8154, -73.0451), (21.316, -157.8677)]
    """

    name = "postalcode_to_latlong"
    input_types = [ColumnSchema(logical_type=PostalCode)]
    return_type = ColumnSchema(logical_type=LatLong)
    filename = "postalcode_to_latlong_data_allCountries.txt"

    def get_function(self):
        file_path = self.get_filepath(self.filename)

        data = pd.read_csv(
            file_path,
            sep="\t",
            usecols=[0, 1, 9, 10],
            header=None,
            names=["country code", "postal code", "latitude", "longitude"],
            dtype={"country code": str, "postal code": str},
        )

        us_df = data[data["country code"] == "US"][
            ["postal code", "latitude", "longitude"]
        ]
        us_df = us_df.reset_index(drop=True)
        us_df.drop_duplicates(subset=["postal code"], inplace=True)
        us_df["latlong"] = list(zip(us_df.latitude, us_df.longitude))

        def postalcode_to_latlong(postalcodes):
            postalcodes_df = pd.DataFrame({"postal code": postalcodes}, dtype=str)
            postalcodes_df["postal code"] = postalcodes_df["postal code"].str[:5]
            postalcodes_df = postalcodes_df.merge(us_df, how="left")
            return postalcodes_df["latlong"]

        return postalcode_to_latlong
