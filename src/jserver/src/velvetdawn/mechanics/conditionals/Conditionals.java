package velvetdawn.mechanics.conditionals;

import velvetdawn.VelvetDawn;
import velvetdawn.models.anytype.AnyJson;

public class Conditionals {

    /** Load the correct conditional class given the dict
     *
     * @param parentId The entity the condition is being attached to.
     * @param data The dictionary of information.
     */
    public static Conditional get(VelvetDawn velvetDawn, String parentId, AnyJson data) throws Exception {
        // TODO Test invalid data type
//        if not isinstance(data, dict):
//            raise errors.ValidationError(f"Conditional items must be a dictionary not '{data}' in {id}")

        if (data.keys().contains("if"))
            return new StandardConditional().fromJson(velvetDawn, parentId, data);
        else if (data.keys().contains("count"))
            return new CountConditional().fromJson(velvetDawn, parentId, data);

        throw new Exception(String.format("Unknown conditional operation '%s' in %s. Please see datapack documentation.", data, parentId));
    }
}
