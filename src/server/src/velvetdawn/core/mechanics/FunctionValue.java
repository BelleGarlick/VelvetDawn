package velvetdawn.core.mechanics;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.mechanics.selectors.Selector;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyFloat;
import velvetdawn.core.models.instances.Instance;

public class FunctionValue {

    /* Function values are the values which conditionals are
        compared to or modify actions are set to. This class
        parses the values to check if it should be random, a
        selector or a specific value.

        Raw value:
         - {"if": '...', "gt": "example"}

        Selector value:
         - {"if": '...', "gt": "@self.attribute"}

        Random value:
         - {"if": '...', "gt": "__rand__"}
    */

    public enum FunctionValueType {
        RAW,
        SELECTOR,
        RANDOM
    }

    private FunctionValueType type = FunctionValueType.RAW;

    public Selector selectorValue;  // Used for type.selector
    public Any rawValue = Any.Null();  // Used for type.raw

    /** Parse the function value to raw, selector or random */
    public FunctionValue(VelvetDawn velvetDawnCore, String parentId, Any value) throws Exception {
        String rawValue = value.toString();

        if (rawValue != null && rawValue.equals("__rand__"))
            this.type = FunctionValueType.RANDOM;

        else if (rawValue != null && rawValue.startsWith("@")) {
            this.type = FunctionValueType.SELECTOR;
            this.selectorValue = Selectors.get(velvetDawnCore, parentId, rawValue.substring(1));
        }

        else {
            this.rawValue = value;
        }
    }

    /** Get the value of the function value */
    public Any value(Instance instance) {
        if (this.type == FunctionValueType.SELECTOR)
            return this.selectorValue.funcGetValue(instance);

        if (this.type == FunctionValueType.RANDOM)
            return new AnyFloat((float) Math.random());

        return this.rawValue;
    }
}
