class Rocket:
    """
    Domain entity representing a Rocket with core attributes
    needed for business logic (e.g., cost per launch, stages).
    """

    def __init__(self, name: str, is_active: bool, cost_per_launch: int, stages: int):
        self.name = name
        self.is_active = is_active
        self.cost_per_launch = cost_per_launch
        self.stages = stages

    def can_reuse(self) -> bool:
        """
        Example domain method: Return True if rocket 
        has at least one reusable stage (fake logic here).
        """
        return self.stages > 1 and self.is_active
