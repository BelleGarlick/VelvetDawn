package velvetdawn.core.models.datapacks;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.mechanics.Triggers;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.instances.attributes.Attributes;
import velvetdawn.core.models.instances.attributes.AttributesDefinition;

import java.util.HashSet;
import java.util.Set;

public class WorldDefinition {

    public final Set<String> tags = new HashSet<>();
    public final AttributesDefinition attributes = new AttributesDefinition();
    public final Triggers triggers = new Triggers();

    /** Parse the world data for the given datapack */
    public void load(VelvetDawn velvetDawn, AnyJson data) throws Exception {
        this.triggers.load(velvetDawn, "world", data
                .get("triggers", new AnyJson())
                .validateInstanceIsJson("Triggers should be a JSON object in the datapack.json"));
    }
}
