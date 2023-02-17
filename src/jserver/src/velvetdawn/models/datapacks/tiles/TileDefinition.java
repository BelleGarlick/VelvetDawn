package velvetdawn.models.datapacks.tiles;

import velvetdawn.VelvetDawn;
import velvetdawn.constants.AttributeKeys;
import velvetdawn.mechanics.Triggers;
import velvetdawn.models.anytype.AnyBool;
import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.models.instances.attributes.Attribute;
import velvetdawn.models.instances.attributes.AttributesDefinition;
import velvetdawn.utils.Json;

import java.util.List;
import java.util.Set;

public class TileDefinition {

    public static Set<String> ValidTileKeys = Set.of(
            "id", "name", "abstract", "extends", "neighbours",
            "movement", "textures", "triggers", "tags", "notes"
    );
    public static Set<String> ValidMovementKeys = Set.of("traversable", "weight", "notes");

    public final String id;
    public final String name;
    public Json neighbours = new Json();
    public final TileTextures textures = new TileTextures();

    public List<String> tags = List.of();
    public final AttributesDefinition attributes = new AttributesDefinition();
    public final Triggers triggers = new Triggers();

    public TileDefinition(String id, String name) {
        this.id = id;
        this.name = name;
    }

    /** Parse the tile movement data, see wiki for more information. */
    public void parseMovement(String datapackId, AttributesDefinition attributes, Json data) throws Exception {
        for (String key: data.keys()) {
            if (!ValidMovementKeys.contains(key))
                throw new Exception(String.format("Invalid movement key '%s' on '%s'", key, datapackId));
        }

        // Extract & Validate
        AnyFloat movementWeight = data.get("weight", new AnyFloat(1))
                .validateInstanceIsFloat(String.format("%s tile movement must be a number", datapackId))
                .validateMinimum(0, String.format("%s tile movement must be at least 0", datapackId));

        AnyBool traversable = data.get("traversable", new AnyBool(true))
                .validateInstanceIsBool(String.format("%s movement traversable must be a boolean", datapackId));

        // Set
        attributes.add(Attribute.builder().id(AttributeKeys.TileTraversable).value(traversable).build());
        attributes.add(Attribute.builder().id(AttributeKeys.TileMovementWeight).value(movementWeight).build());
    }

    public static TileDefinition loadFromJson(VelvetDawn velvetDawn, String datapackId, Json json) throws Exception {
        for (String key: json.keys()) {
            if (!ValidTileKeys.contains(key))
                throw new Exception(String.format("Invalid key '%s' on entity '%s'", key, datapackId));
        }

        var tile = new TileDefinition(
                datapackId,
                json.get("name")
                    .validateInstanceIsString(String.format("%s name is invalid", datapackId))
                    .value
        );

        tile.neighbours = json.getJson("neighbours", new Json(), String.format("Tile %s has invalid neighbours. Neighbours must be a json object.", datapackId));

        tile.parseMovement(datapackId, tile.attributes, json.getJson("movement", new Json(),
                String.format("%s movement must be a json object", datapackId)));

        tile.textures.load(datapackId, json.getJson("textures", new Json(),
                String.format("Tile textures must be a Json obejct found error in %s.", datapackId)));

        tile.triggers.load(velvetDawn, datapackId, json.getJson("triggers", new Json(), String.format(
                "Triggers in '%s' are invalid. Triggers must be a json object.", datapackId)));

        tile.tags = json.getStringList("tags", List.of(), String.format(
                "Tags in '%s' are invalid. Tags must be a list of strings.", datapackId));

        tile.attributes.load(velvetDawn, datapackId, json);

        return tile;
    }
}
