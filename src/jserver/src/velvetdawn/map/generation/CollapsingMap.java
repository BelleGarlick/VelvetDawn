package velvetdawn.map.generation;

import org.jetbrains.annotations.NotNull;
import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.models.datapacks.tiles.TileDefinition;
import velvetdawn.models.instances.TileInstance;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class CollapsingMap {

    private final VelvetDawn velvetDawn;
    private final Config config;

    public final Map<Integer, Map<Integer, Set<String>>> map = new HashMap<>();

    public CollapsingMap(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;

        for (int i = 0; i < config.map.width; i++) {
            if (!this.map.containsKey(i))
                this.map.put(i, new HashMap<>());

            for (int j = 0; j < config.map.height; j++) {
                this.map.get(i).put(j, new HashSet<>(
                        velvetDawn.datapacks.tiles
                                .values()
                                .stream()
                                .map(tile -> tile.id)
                                .collect(Collectors.toSet())
                ));
            }
        }
    }

    @NotNull
    public boolean has(Coordinate coord) {
        return map.containsKey(coord.tileX()) && map.get(coord.tileX()).containsKey(coord.tileY());
    }

    public void set(Coordinate coord, Set<String> items) {
        if (!map.containsKey(coord.tileX()))
            map.put(coord.tileX(), new HashMap<>());
        map.get(coord.tileX()).put(coord.tileY(), items);
    }

    public Set<String> get(Coordinate cell) {
        if (map.containsKey(cell.tileX()) && map.get(cell.tileX()).containsKey(cell.tileY()))
            return map.get(cell.tileX()).get(cell.tileY());
        return null;
    }

    public Map<Integer, Map<Integer, TileInstance>> toTiles() {
        // TODO Test that variants and colours are picked in test
        Map<Integer, Map<Integer, TileInstance>> tiles = new HashMap<>();

        for (int col = 0; col < config.map.width; col++) {
            tiles.put(col, new HashMap<>());

            for (int row = 0; row < config.map.height; row++) {
                String item = (String) this.get(new Coordinate(col, row)).toArray()[0];

                TileInstance tile = new TileInstance("%s-%s", item, new Coordinate(col, row));
                TileDefinition tileDef = velvetDawn.datapacks.tiles.get(item);
                tileDef.attributes.instantiateInstanceAttributes(tile);
                tile.tags.addAll(tileDef.tags);
                tile.attributes.set("texture.color", tileDef.textures.chooseColor());
                tile.attributes.set("texture.background", tileDef.textures.chooseImage());

                tiles.get(col).put(row, tile);
            }
        }

        return tiles;
    }
}
