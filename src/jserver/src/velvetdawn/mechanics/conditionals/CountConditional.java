package velvetdawn.mechanics.conditionals;

import velvetdawn.models.instances.Instance;

public class CountConditional extends Conditional {

    /** Comparison class to compare the amount of selected items */

    public CountConditional() {
        super("count", false);
    }

    /** Test the comparison */
    public boolean isTrue(Instance instance) {
        int count = this.selector.getChainedSelection(instance).size();

        switch (this.function) {
            case EQUALS:
                return count == this.functionValue.value(instance).toNumber();

            case NOT_EQUALS:
                return count != this.functionValue.value(instance).toNumber();

            case LESS_THAN:
                return count < this.functionValue.value(instance).toNumber();

            case LESS_THAN_EQUAL:
                return count <= this.functionValue.value(instance).toNumber();

            case GREATER_THAN:
                return count > this.functionValue.value(instance).toNumber();

            case GREATER_THAN_EQUAL:
                return count >= this.functionValue.value(instance).toNumber();
        }

        return false;
    }
}
