package velvetdawn.mechanics.conditionals;

import velvetdawn.models.instances.Instance;

public class StandardConditional extends Conditional {

    /*
     This type of conditional compares if the selector matches the given value """
     */

    public StandardConditional() {
        super("if");
    }

    /** Compare the values in the selector */
    public boolean isTrue(Instance instance) {
        switch (this.function) {
            case EQUALS:
                return this.selector.funcEquals(instance, this.functionValue.value(instance));

            case NOT_EQUALS:
                return !this.selector.funcEquals(instance, this.functionValue.value(instance));

            case LESS_THAN:
                return this.selector.funcLessThan(instance, this.functionValue.value(instance));

            case LESS_THAN_EQUAL:
                return this.selector.funcLessThanEqual(instance, this.functionValue.value(instance));

            case GREATER_THAN:
                return !this.selector.funcLessThanEqual(instance, this.functionValue.value(instance));

            case GREATER_THAN_EQUAL:
                return !this.selector.funcLessThan(instance, this.functionValue.value(instance));

            case HAS_TAG:
                return this.selector.funcHasTag(instance, this.functionValue.value(instance));

            case NOT_HAS_TAG:
                return !this.selector.funcHasTag(instance, this.functionValue.value(instance));
        }

        return false;
    }
}
