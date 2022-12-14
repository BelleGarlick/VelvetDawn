

class ValidationError(Exception):
    pass


class UnknownEntityError(Exception):
    def __init__(self, entity: str):
        Exception.__init__(self, f"Unknown entity id '{entity}'")


class EntityMissingFromSetupDefinition(Exception):
    def __init__(self, entity):
        Exception.__init__(self, f"Entity missing from setup definition '{entity}'")
