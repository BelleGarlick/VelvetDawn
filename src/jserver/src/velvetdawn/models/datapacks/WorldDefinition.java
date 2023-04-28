package velvetdawn.models.datapacks;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.Triggers;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.instances.attributes.Attributes;

import java.util.HashSet;
import java.util.Set;

public class WorldDefinition {

    public final Set<String> tags = new HashSet<>();
    public final Attributes attributes = new Attributes();
    public final Triggers triggers = new Triggers();

    /** Parse the world data for the given datapack */
    public void load(VelvetDawn velvetDawn, AnyJson data) throws Exception {
        this.triggers.load(velvetDawn, "world", data
                .get("triggers", new AnyJson())
                .validateInstanceIsJson("Triggers should be a JSON object in the datapack.json"));
    }
}
