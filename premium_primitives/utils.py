import os.path


class PremiumDataMixin:
    def get_filepath(self, filename):
        import featuretools as ft

        data_folder = ft.config.get("premium_primitives_data_folder")
        return os.path.join(data_folder, filename)
