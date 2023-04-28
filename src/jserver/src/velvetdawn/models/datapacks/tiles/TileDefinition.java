package velvetdawn.models.datapacks.tiles;

import velvetdawn.VelvetDawn;
import velvetdawn.constants.AttributeKeys;
import velvetdawn.mechanics.Triggers;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyBool;
import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.instances.attributes.Attribute;
import velvetdawn.models.instances.attributes.AttributesDefinition;

import java.util.HashSet;
import java.util.Set;

public class TileDefinition {

    public static Set<String> ValidTileKeys = Set.of(
            "id", "name", "abstract", "extends", "neighbours",
            "movement", "textures", "triggers", "tags", "notes"
    );
    public static Set<String> ValidMovementKeys = Set.of("traversable", "weight", "notes");

    public final String id;
    public final String name;
    public AnyJson neighbours = new AnyJson();
    public final TileTextures textures = new TileTextures();

    public Set<String> tags = new HashSet<>();
    public final AttributesDefinition attributes = new AttributesDefinition();
    public final Triggers triggers = new Triggers();

    public TileDefinition(String id, String name) {
        this.id = id;
        this.name = name;
    }

    /** Parse the tile movement data, see wiki for more information. */
    public void parseMovement(String datapackId, AttributesDefinition attributes, AnyJson data) throws Exception {
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

    public static TileDefinition loadFromJson(VelvetDawn velvetDawn, String datapackId, AnyJson json) throws Exception {
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

        tile.neighbours = json
                .get("neighbours", new AnyJson())
                .validateInstanceIsJson(String.format("Tile %s has invalid neighbours. Neighbours must be a json object.", datapackId));

        tile.parseMovement(datapackId, tile.attributes, json
                .get("movement", new AnyJson())
                .validateInstanceIsJson(String.format("%s movement must be a json object", datapackId)));

        tile.textures.load(datapackId, json
                .get("textures", new AnyJson())
                .validateInstanceIsJson(String.format("Tile textures must be a AnyJson object found error in %s.", datapackId)));

        tile.triggers.load(velvetDawn, datapackId, json
                .get("triggers", new AnyJson())
                .validateInstanceIsJson(String.format("Triggers in '%s' are invalid. Triggers must be a json object.", datapackId)));

        var tags = json.get("tags", Any.list())
                .validateInstanceIsList(String.format("Tags in '%s' are invalid. Tags must be a list of strings.", datapackId));

        for (Any item: tags.items)
            tile.tags.add(item
                    .validateInstanceIsString(String.format("Error in %s. Tags must be strings.", datapackId))
                    .toString());

        tile.attributes.load(velvetDawn, datapackId, json);

        return tile;
    }
}
