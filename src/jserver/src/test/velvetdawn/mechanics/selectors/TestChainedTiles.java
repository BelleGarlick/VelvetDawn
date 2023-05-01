package test.velvetdawn.mechanics.selectors;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.mechanics.selectors.tiles.SelectorTile;
import velvetdawn.core.mechanics.selectors.tiles.SelectorTiles;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.instances.WorldInstance;

import java.util.ArrayList;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;


public class TestChainedTiles extends BaseTest {

    @Test
    public void test_selector_tile() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);
        var tile = velvetDawn.map.getTile(new Coordinate(5, 0));

        var selector = Selectors.get(velvetDawn, unit.datapackId, "tile");
        var selectorTiles = Selectors.get(velvetDawn, unit.datapackId, "tiles");
        assertTrue(selector instanceof SelectorTile);
        assertTrue(selectorTiles instanceof SelectorTiles);

        var oneTileFromUnit = selector.getChainedSelection(unit);
        var oneTileFromTile = selector.getChainedSelection(tile);
        var oneTileFromWorld = selector.getChainedSelection(WorldInstance.getInstance());
        assertEquals(1, oneTileFromUnit.size());
        assertEquals(1, oneTileFromTile.size());
        assertEquals(0, oneTileFromWorld.size());
        assertEquals(tile.datapackId, new ArrayList<>(oneTileFromUnit).get(0).datapackId);
        assertEquals(tile.datapackId, new ArrayList<>(oneTileFromTile).get(0).datapackId);

        assertEquals(121, selectorTiles.getChainedSelection(unit).size());
        assertEquals(121, selectorTiles.getChainedSelection(tile).size());
        assertEquals(121, selectorTiles.getChainedSelection(WorldInstance.getInstance()).size());
    }
}
