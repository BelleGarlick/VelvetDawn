package velvetdawn.map;

import velvetdawn.constants.AttributeKeys;
import velvetdawn.map.generation.MapGeneration;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;
import velvetdawn.map.spawn.Spawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.instances.EntityInstance;
import velvetdawn.models.instances.TileInstance;
import velvetdawn.models.instances.TileInstanceUpdate;
import velvetdawn.models.map.Chunk;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

public class MapManager {

    private final VelvetDawn velvetDawn;
    private final Config config;

//    private final Map<Integer, Map<Integer, Chunk>> chunks = new HashMap<>();
    private Chunk chunk;

    public final Spawn spawn;

    public MapManager(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;

        this.spawn = new Spawn(velvetDawn, config);
    }

    public Chunk getChunk(int chunkX, int chunkY) {
        return chunk;
//        if (this.chunks.containsKey(chunkX) && this.chunks.get(chunkX).containsKey(chunkY))
//            return this.chunks.get(chunkX).get(chunkY);
//        return null;
    }

    public TileInstance getTile(Coordinate position) {
        var chunk = this.getChunk(position.tileX() / Chunk.SIZE, position.tileY() / Chunk.SIZE);
        if (chunk != null) {
            return chunk.getTileFromAbsoluteTilePosition(position.tileX(), position.tileY());
        }

        return null;
    }

    public List<Chunk> listChunks() {
        if (this.chunk == null)
            return List.of();

        return List.of(this.chunk);
//                .stream()
//                .map(Region::listChunks)
//                .flatMap(Collection::stream)
//                .collect(Collectors.toList());
    }

    public List<TileInstance> listTiles() {
        return this.listChunks()
                .stream()
                .map(Chunk::listTiles)
                .flatMap(Collection::stream)
                .collect(Collectors.toList());
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
    public int getDistance(Coordinate from, Coordinate to) {
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

        return List.of(
            new Coordinate(point.tileX() - 1, isOdd ? point.tileY() : point.tileY() - 1),
            new Coordinate(point.tileX() - 1, isOdd ? point.tileY() + 1 : point.tileY()),
            new Coordinate(point.tileX(), point.tileY() - 1),
            new Coordinate(point.tileX(), point.tileY() + 1),
            new Coordinate(point.tileX() + 1, isOdd ? point.tileY() : point.tileY() - 1),
            new Coordinate(point.tileX() + 1, isOdd ? point.tileY() + 1 : point.tileY())
        );
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
        MapGeneration map = new MapGeneration();
        this.chunk = map.generate(velvetDawn, config);
    }

    public List<TileInstanceUpdate> getUpdatesBroadcast(boolean fullState) {
        // todo needs implememtning
        return List.of();
    }
}
