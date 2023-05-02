package velvetdawn.map;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.VelvetDawn;
import velvetdawn.core.map.MapManager;
import velvetdawn.core.models.Coordinate;

import static junit.framework.TestCase.assertEquals;

public class TestMap extends BaseTest {

    @Test
    public void testGetDistance() throws Exception {
        // Check correct distances
        assertEquals(15, MapManager.getDistance(new Coordinate(0, 0), new Coordinate(10, 10)));
        assertEquals(10, MapManager.getDistance(new Coordinate(10, 0), new Coordinate(10, 10)));
        assertEquals(4, MapManager.getDistance(new Coordinate(7, 7), new Coordinate(10, 10)));

        assertEquals(14, MapManager.getDistance(new Coordinate(0, 0), new Coordinate(7, 10)));
        assertEquals(12, MapManager.getDistance(new Coordinate(10, 0), new Coordinate(7, 10)));
        assertEquals(3, MapManager.getDistance(new Coordinate(7, 7), new Coordinate(7, 10)));
    }

    @Test
    public void testGetNeighbours() throws Exception {
        var config = this.getConfig();
        var velvetDawn = new VelvetDawn(config);

        assertEquals(2, velvetDawn.map.getNeighbours(new Coordinate()).size());
        assertEquals(6, velvetDawn.map.getNeighbours(new Coordinate(2, 2)).size());
        assertEquals(0, velvetDawn.map.getNeighbours(new Coordinate(20, 20)).size());
        assertEquals(3, velvetDawn.map.getNeighbours(new Coordinate(10, 10)).size());
    }

    @Test
    public void getNeighboursInRange() throws Exception {
        var config = this.getConfig();
        var velvetDawn = new VelvetDawn(config);

        var coord = new Coordinate(2, 2);

        assertEquals(1, velvetDawn.map.getNeighboursInRange(coord, 0).size());
        assertEquals(7, velvetDawn.map.getNeighboursInRange(coord, 1).size());
        assertEquals(19, velvetDawn.map.getNeighboursInRange(coord, 2).size());
    }
}
