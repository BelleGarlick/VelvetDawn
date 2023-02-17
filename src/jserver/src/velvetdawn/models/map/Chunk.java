package velvetdawn.models.map;

import velvetdawn.models.instances.TileInstance;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Chunk {

    public static final int SIZE = 32;

//    public final int chunkX;
//    public final int chunkY;
    public Map<Integer, Map<Integer, TileInstance>> tiles = new HashMap<>();

    public Chunk() {
    }

//    public Coordinate getWorldPosition() {
//        return new Coordinate(
//                this.chunkX * Chunk.SIZE,
//                this.chunkY * Chunk.SIZE
//        );
//    }

    public TileInstance getTileFromRelativeCoordinate(int relX, int relY) {
        if (this.tiles.containsKey(relX) && this.tiles.get(relX).containsKey(relY))
            return this.tiles.get(relX).get(relY);
        return null;
    }

    public TileInstance getTileFromAbsoluteTilePosition(int absTileX, int absTileY) {
//        int relTileX = absTileX - this.chunkX * Chunk.SIZE;
//        int relTileY = absTileY - this.chunkY * Chunk.SIZE;

//        return this.getTileFromRelativeCoordinate(relTileX, relTileY);
        return this.getTileFromRelativeCoordinate(absTileX, absTileY);
    }

    public List<TileInstance> listTiles() {
        return this.tiles.values()
                .stream()
                .map(Map::values)
                .flatMap(Collection::stream)
                .collect(Collectors.toList());
    }

    public void setTile(TileInstance tile) {
        if (!this.tiles.containsKey(tile.position.tileX()))
            this.tiles.put(tile.position.tileX(), new HashMap<>());

        this.tiles.get(tile.position.tileX()).put(
                tile.position.tileY(),
                tile
        );
    }
}
