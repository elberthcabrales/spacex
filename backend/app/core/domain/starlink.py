class Starlink:
    """
    Domain entity for a Starlink satellite.
    """

    def __init__(self, object_name: str, country_code: str):
        self.object_name = object_name
        self.country_code = country_code
