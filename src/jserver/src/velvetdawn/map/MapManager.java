package velvetdawn.map;

import velvetdawn.constants.AttributeKeys;
import velvetdawn.map.generation.MapGeneration;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;
import velvetdawn.map.spawn.Spawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.instances.entities.EntityInstance;
import velvetdawn.models.instances.TileInstance;
import velvetdawn.models.instances.TileInstanceUpdate;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MapManager {

    private final VelvetDawn velvetDawn;
    private final Config config;

    private Map<Integer, Map<Integer, TileInstance>> map = new HashMap<>();

    public final Spawn spawn;

    public MapManager(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;

        this.spawn = new Spawn(velvetDawn, config);
    }

    public TileInstance getTile(Coordinate position) {
        if (this.map.containsKey(position.tileX())) {
            return this.map.get(position.tileX()).getOrDefault(position.tileY(), null);
        }

        return null;
    }

    public List<TileInstance> listTiles() {
        return this.map.values()
                .stream()
                .map(Map::values)
                .flatMap(Collection::stream)
                .collect(Collectors.toList());
    }

    public Map<Integer, Map<Integer, TileInstance>> getTiles() {
        return this.map;
    }

    public Collection<EntityInstance> getEntitiesAtPosition(Coordinate position) {
        return List.of();
    }

    /** Calculate the distance between two positions. This function
     * is designed for flat-top hexagons where the second column
     * is sunk vertically. Changes to that layout will require changes
     * to this function.
     * This function is also implemented in the FE for
     * combat and targeting.
     *
     * @param from Point a
     * @param to Poiny b
     * @return Number of hexagons between the two files
     */
    public static int getDistance(Coordinate from, Coordinate to) {
        int dcol = Math.abs(from.tileX() - to.tileX());
        int drow = Math.abs(from.tileY() - to.tileY());

        float distance = Math.max(dcol, drow + dcol / 2f);

        if (from.tileX() % 2 == 0 && dcol % 2 == 1) {
            if (to.y <= from.tileY())
               return (int) Math.floor(distance);
            return (int) Math.ceil(distance);
        }

        else if (dcol % 2 == 1) {
            if (to.y <= from.tileY())
                return (int) Math.ceil(distance);
            return (int) Math.floor(distance);
        }

        return (int) distance;
    }

    public List<Coordinate> getNeighbours(Coordinate point) {
        boolean isOdd = point.tileX() % 2 == 1;

        return Stream.of(
            new Coordinate(point.tileX() - 1, isOdd ? point.tileY() : point.tileY() - 1),
            new Coordinate(point.tileX() - 1, isOdd ? point.tileY() + 1 : point.tileY()),
            new Coordinate(point.tileX(), point.tileY() - 1),
            new Coordinate(point.tileX(), point.tileY() + 1),
            new Coordinate(point.tileX() + 1, isOdd ? point.tileY() : point.tileY() - 1),
            new Coordinate(point.tileX() + 1, isOdd ? point.tileY() + 1 : point.tileY())
        )
                .filter(p -> p.tileX() >= 0
                        && p.tileX() < config.map.width
                        && p.tileY() >= 0
                        && p.tileY() < config.map.height)
                .collect(Collectors.toList());
    }

    public boolean isTraversable(Coordinate point) {
        TileInstance tile = this.getTile(point);

        if (tile != null) {
            Any value = tile.attributes.get(AttributeKeys.TileTraversable);
            if (value instanceof AnyFloat)
                return value.toNumber() == 1;
        }

        return false;
    }

    public void generate() throws Exception {
        this.spawn.assignSpawnPoints();
        MapGeneration map = new MapGeneration(velvetDawn, config);
        this.map = map.generate();
    }

    public List<TileInstanceUpdate> getUpdatesBroadcast(boolean fullState) {
        // todo needs implememtning
        return List.of();
    }
}
