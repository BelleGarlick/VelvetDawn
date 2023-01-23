from velvet_dawn.db.instances import Instance
from velvet_dawn.mechanics.conditionals.conditional import Comparison, Conditional


class ConditionalCounting(Conditional):
    """ Comparison class to compare the amount of selected items """

    def __init__(self):
        super().__init__(keyword="count", has_tag_enabled=False)

    def is_true(self, instance: Instance) -> bool:
        """ Test the comparison """
        count = len(self.selector.get_chained_selection(instance))

        if self.function == Comparison.EQUALS:
            return count == int(self.function_value.value(instance))

        if self.function == Comparison.NOT_EQUALS:
            return count != int(self.function_value.value(instance))

        if self.function == Comparison.LESS_THAN:
            return count < int(self.function_value.value(instance))

        if self.function == Comparison.LESS_THAN_EQUAL:
            return count <= int(self.function_value.value(instance))

        if self.function == Comparison.GREATER_THAN:
            return count > int(self.function_value.value(instance))

        if self.function == Comparison.GREATER_THAN_EQUAL:
            return count >= int(self.function_value.value(instance))

        return False
