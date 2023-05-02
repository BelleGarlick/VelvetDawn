package velvetdawn.map;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.map.MapManager;
import velvetdawn.core.models.Coordinate;

import static junit.framework.TestCase.assertEquals;

public class TestMap extends BaseTest {

    @Test
    public void test_get_distance() throws Exception {
        // Check correct distances
        assertEquals(15, MapManager.getDistance(new Coordinate(0, 0), new Coordinate(10, 10)));
        assertEquals(10, MapManager.getDistance(new Coordinate(10, 0), new Coordinate(10, 10)));
        assertEquals(4, MapManager.getDistance(new Coordinate(7, 7), new Coordinate(10, 10)));

        assertEquals(14, MapManager.getDistance(new Coordinate(0, 0), new Coordinate(7, 10)));
        assertEquals(12, MapManager.getDistance(new Coordinate(10, 0), new Coordinate(7, 10)));
        assertEquals(3, MapManager.getDistance(new Coordinate(7, 7), new Coordinate(7, 10)));
    }
}
