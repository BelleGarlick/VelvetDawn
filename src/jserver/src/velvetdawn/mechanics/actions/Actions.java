package velvetdawn.mechanics.actions;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.conditionals.Conditionals;
import velvetdawn.utils.Json;

import java.util.List;

public class Actions {

    /* This module is the entry point for getting an action given a string.
    The class will be chosen based on keys in the dict then return the parsed
    action based on the dict.

    Examples:
        {"if": [...], "modify": "self.health", "set": 5} -> set the health of the unit to 5
    */

    /** Given the dict, decide which action class should be used
     *
     * @param parentId The id of the entity attached to this action
     * @param data The dictionary defining which action should be used
     * @return The chosen action object
     */
    public static Action fromJson(VelvetDawn velvetDawn, String parentId, Json data) throws Exception {
        // TODO Validate what happens if not a data object
//        if not isinstance(data, dict)
//            raise errors.ValidationError(f"Invalid actionable in {id}. '{data}' must be a dictionary")

        Action builtAction = null;
        if (data.keys().contains("modify"))
            builtAction = ActionModify.fromJson(velvetDawn, parentId, data);

        if (builtAction == null)
            throw new Exception(String.format("Invalid action '%s' on %s", data, parentId));

        // Create the comparison objects
        var conditions = data.getStrictJsonList("conditions", List.of(), String.format("Conditionals in actions must be a list of json objects (%s)", parentId));
        for (Json condition: conditions)
            builtAction.addCondition(Conditionals.get(velvetDawn, parentId, condition));

        return builtAction;
    }
}
