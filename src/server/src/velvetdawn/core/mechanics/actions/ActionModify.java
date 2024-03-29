package velvetdawn.core.mechanics.actions;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.mechanics.FunctionValue;
import velvetdawn.core.mechanics.selectors.Selector;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.instances.Instance;

import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;

public class ActionModify extends Action {

    /* The action modify class, responsible for modifying
    attributes of selector attached.
    */

    public enum ActionModifierFunction {
        Set,
        Add,
        Sub,
        Mul,
        Reset,
        AddTag,
        RemoveTag
    }

    /** The key:function map defined in the datapack dictionary */
    public static Map<String, ActionModifierFunction> KeyMap = Map.of(
            "set", ActionModifierFunction.Set,
            "add", ActionModifierFunction.Add,
            "sub", ActionModifierFunction.Sub,
            "subtract", ActionModifierFunction.Sub,
            "mul", ActionModifierFunction.Mul,
            "multiply", ActionModifierFunction.Mul,
            "reset", ActionModifierFunction.Reset,
            "add-tag", ActionModifierFunction.AddTag,
            "remove-tag", ActionModifierFunction.RemoveTag
    );

    public static Set<ActionModifierFunction> NON_ATTRIBUTE_MODIFIERS = Set.of(
            ActionModifierFunction.AddTag, ActionModifierFunction.RemoveTag
    );

    private Selector selector;
    public ActionModifierFunction function = ActionModifierFunction.Set;
    private FunctionValue functionValue = null;

    /** Parse the dict of tile/unit data to construct this action */
    public static ActionModify fromJson(VelvetDawn velvetDawn, String parentId, AnyJson data) throws Exception {
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
        switch (this.function) {
            case Set:
                this.selector.funcSet(instance, this.functionValue.value(instance));
                break;
            case Add:
                this.selector.funcAdd(instance, this.functionValue.value(instance));
                break;
            case Mul:
                this.selector.funcMul(instance, this.functionValue.value(instance));
                break;
            case Sub:
                this.selector.funcSub(instance, this.functionValue.value(instance));
                break;
            case Reset:
                this.selector.funcReset(instance, this.functionValue.value(instance));
                break;
            case AddTag:
                this.selector.funcAddTag(instance, this.functionValue.value(instance));
                break;
            case RemoveTag:
                this.selector.funcRemoveTag(instance, this.functionValue.value(instance));
                break;
            default:
                throw new Exception(String.format("Unknown action function type: '%s'", this.function));
        }
    }
}
