class Launch:
    """
    Domain entity for a Launch, which references a rocket by ID.
    """

    def __init__(self, details: str, success: bool, rocket_id: int):
        self.details = details
        self.success = success
        self.rocket_id = rocket_id

    def is_successful(self) -> bool:
        return self.success
