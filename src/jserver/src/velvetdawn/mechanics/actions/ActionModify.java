package velvetdawn.mechanics.actions;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.FunctionValue;
import velvetdawn.mechanics.selectors.Selector;
import velvetdawn.mechanics.selectors.Selectors;
import velvetdawn.models.instances.Instance;
import velvetdawn.utils.Json;

import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

public class ActionModify extends Action {

    /* The action modify class, responsible for modifying
    attributes of selector attached.
    */

    public enum ActionModifierFunction {
        SET,
        ADD,
        SUB,
        MUL,
        RESET,
        ADD_TAG,
        REMOVE_TAG
    }

    /** The key:function map defined in the datapack dictionary */
    public static Map<String, ActionModifierFunction> KeyMap = Map.of(
            "set", ActionModifierFunction.SET,
            "add", ActionModifierFunction.ADD,
            "sub", ActionModifierFunction.SUB,
            "subtract", ActionModifierFunction.SUB,
            "mul", ActionModifierFunction.MUL,
            "multiply", ActionModifierFunction.MUL,
            "reset", ActionModifierFunction.RESET,
            "add-tag", ActionModifierFunction.ADD_TAG,
            "remove-tag", ActionModifierFunction.REMOVE_TAG
    );

    public static Set<ActionModifierFunction> NON_ATTRIBUTE_MODIFIERS = Set.of(
            ActionModifierFunction.ADD_TAG, ActionModifierFunction.REMOVE_TAG
    );

    private Selector selector;
    public ActionModifierFunction function = ActionModifierFunction.SET;
    private FunctionValue functionValue = null;

    /** Parse the dict of tile/unit data to construct this action */
    public static ActionModify fromJson(VelvetDawn velvetDawn, String parentId, Json data) throws Exception {
        if (!data.containsKey("modify")) {
            throw new Exception("Modify functions must contain a 'modify' selector");
        }

        // Check the number of functions is valid
        AtomicInteger totalFunctionKeys = new AtomicInteger();
        KeyMap.forEach((key, value) -> totalFunctionKeys.addAndGet(data.containsKey(key) ? 1 : 0));
        if (totalFunctionKeys.get() != 1) {
            // TODO Test this error formats correct
            throw new Exception(
                    String.format(
                            "Invalid modify action on %s. Modify actions must contain one of %s. Problem data: %s",
                            parentId,
                            data.keys(),
                            data.toString()
                    )
            );
        }

        // Construct the action and it's function
        ActionModify action = new ActionModify();
        action.selector = Selectors.get(velvetDawn, parentId,
                data.get("modify")
                        .validateInstanceIsString(String.format("Modify value on action in '%s' must be a string as a selector", parentId))
                        .value
        );


        // Find the key used and update the function (we already verify there is a key above)
        String functionKey = null;
        for (String key: data.keys()) {
            if (KeyMap.containsKey(key)) {
                functionKey = key;
                // TODO Test if not string
                action.functionValue = new FunctionValue(velvetDawn, parentId, data.get(key));
                action.function = KeyMap.get(key);
            }
        }

        // If a non-attribute modifier is used with an attribute or no attribute is
        // given to an attribute modifier then throw an error
        if (NON_ATTRIBUTE_MODIFIERS.contains(action.function)) {
            if (action.selector.attribute != null)
                throw new Exception(String.format(
                        "Action '%s' tags cannot be performed on a selector with attributes '%s'",
                        functionKey,
                        data.get("modify").validateInstanceIsString("Modify selector must be a string").value
                ));
        } else if (action.selector.attribute == null)
            throw new Exception(
                    String.format(
                        "Modify actions must ensure the selectors modify an attribute not '%s'",
                        data.get("modify").validateInstanceIsString("Modify selector must be a string").value
                    ));

        return action;
    }

    /** Execute the attribute */
    public void run(Instance instance) throws Exception {
        if (this.function == ActionModifierFunction.SET)
            this.selector.funcSet(instance, this.functionValue.value(instance));

        else if (this.function == ActionModifierFunction.ADD)
            this.selector.funcAdd(instance, this.functionValue.value(instance));

        else if (this.function == ActionModifierFunction.MUL)
            this.selector.funcMul(instance, this.functionValue.value(instance));

        else if (this.function == ActionModifierFunction.SUB)
            this.selector.funcSub(instance, this.functionValue.value(instance));

        else if (this.function == ActionModifierFunction.RESET)
            this.selector.funcReset(instance, this.functionValue.value(instance));

        else if (this.function == ActionModifierFunction.ADD_TAG)
            this.selector.funcAddTag(instance, this.functionValue.value(instance));

        else if (this.function == ActionModifierFunction.REMOVE_TAG)
            this.selector.funcRemoveTag(instance, this.functionValue.value(instance));

        else
            throw new Exception(String.format("Unknown action function type: '%s'", this.function));
    }
}
