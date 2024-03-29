package velvetdawn.core.map;

import velvetdawn.core.constants.AttributeKeys;
import velvetdawn.core.map.generation.MapGeneration;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyFloat;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.VelvetDawn;
import velvetdawn.core.map.spawn.Spawn;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.entities.EntityInstance;
import velvetdawn.core.models.instances.TileInstance;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MapManager {

    private final VelvetDawn velvetDawn;
    private final Config config;
    public int width;
    public int height;

    private ArrayList<ArrayList<TileInstance>> map = new ArrayList<>();

    public final Spawn spawn;

    public MapManager(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;

        this.width = config.map.width;
        this.height = config.map.height;
        this.spawn = new Spawn(velvetDawn, config);
    }

    public TileInstance getTile(Coordinate position) {
        var row = this.map.get(position.tileX());
        if (row == null)
            return null;

        return row.get(position.tileY());
    }

    public List<TileInstance> listTiles() {
        return this.map
                .stream()
                .flatMap(Collection::stream)
                .collect(Collectors.toList());
    }

    public ArrayList<ArrayList<TileInstance>> getTiles() {
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
                        && p.tileX() < this.width
                        && p.tileY() >= 0
                        && p.tileY() < this.height)
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

    /** Get all tiles within a range from a target coordinate
     *
     * @param target Target coordinate
     * @param range Number of ranks to search
     * @return All neighbours within range of the target
     */
    public Set<Coordinate> getNeighboursInRange(Coordinate target, int range) {
        Set<Coordinate> neighbours = new HashSet<>();
        var previousRank = Set.of(target);

        neighbours.add(target);

        for (int n = 0; n < range; n++) {
            var rankNeighbours = previousRank.stream()
                    .map(this::getNeighbours)
                    .flatMap(Collection::stream)
                    .filter(x -> !neighbours.contains(x))
                    .collect(Collectors.toSet());

            neighbours.addAll(rankNeighbours);
            previousRank = rankNeighbours;
        }

        return neighbours;
    }
}
