package test.velvetdawn.map.spawn;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;

import java.util.stream.Collectors;

import static junit.framework.TestCase.assertFalse;
import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;

public class TestSpawn extends BaseTest {


    /** We know all other parts work, so here were just test the correct number
     *  of tiles are created to the db per team */
    @Test
    public void testAllocateSpawnPoints() throws Exception {
        var config = new Config();
        config.map.height = 14;
        config.map.width = 14;
        config.spawn.spawnRadiusMultiplier = 0;
        config.spawn.baseSpawnRadius = 0;
        var velvetDawn = new VelvetDawn(config);

        velvetDawn.players.join("abc", "a");
        velvetDawn.players.join("bcd", "a");
        velvetDawn.map.spawn.assignSpawnPoints();

        var items = velvetDawn.map.spawn
                .listAllSpawnPoints()
                .stream()
                .sorted((a, b) -> Float.compare(a.y, b.y))
                .collect(Collectors.toList());

        assertEquals(2, items.size());
        assertEquals(7, items.get(0).x, 0);
        assertEquals(0, items.get(0).y, 0);
        assertEquals(6, items.get(1).x, 0);
        assertEquals(13, items.get(1).y, 0);
    }

    /** Same test as above but with different teams/sizes */
    @Test
    public void testAllocateSpawnPoints2() throws Exception {
        var config = new Config();
        config.map.height = 20;
        config.map.width = 20;
        config.spawn.spawnRadiusMultiplier = 2;
        config.spawn.baseSpawnRadius = 3;
        var velvetDawn = new VelvetDawn(config);

        var player1 = velvetDawn.players.join("abc", "a");
        var player2 = velvetDawn.players.join("bcd", "a");
        velvetDawn.map.spawn.assignSpawnPoints();

        assertEquals(22, velvetDawn.map.spawn.listAllSpawnPoints().size());
        assertEquals(11, velvetDawn.map.spawn.getSpawnCoordinatesForPlayer(player1).size());
        assertTrue(velvetDawn.map.spawn.isPointSpawnable(player1, new Coordinate(10, 0)));
        assertFalse(velvetDawn.map.spawn.isPointSpawnable(player1, new Coordinate(0, 0)));

        assertEquals(11, velvetDawn.map.spawn.getSpawnCoordinatesForPlayer(player2).size());
        assertTrue(velvetDawn.map.spawn.isPointSpawnable(player2, new Coordinate(10, 19)));
        assertFalse(velvetDawn.map.spawn.isPointSpawnable(player2, new Coordinate(0, 19)));
    }

}