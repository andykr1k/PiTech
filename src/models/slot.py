
class Slot:
    def __init__(self, state="UNUSED", container=None):
        """
       The state of the slot - "NAN", "UNUSED", or "CONTAINER".
        """
        self.state = state
        self.container = container

    def __repr__(self):
        if self.state == "CONTAINER" and self.container:
            return f"{self.container}"
        return self.state