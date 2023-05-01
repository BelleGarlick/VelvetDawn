package test.velvetdawn.map.spawn;

import org.junit.Test;
import velvetdawn.core.VelvetDawn;
import velvetdawn.core.map.spawn.BorderSpawnMode;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.models.config.SpawnConfig;

import java.util.List;

import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertThrows;


public class TestBorderSpawn extends test.BaseTest {

    @Test
    public void test_lobby_to_setup_create_spawn() throws Exception {
        var velvetDawn = new VelvetDawn(this.getConfig());

        assertEquals(0, velvetDawn.map.spawn.listAllSpawnPoints().size());

        velvetDawn.players.join("abc", "a");
        velvetDawn.players.join("bcd", "a");

        velvetDawn.game.startSetupPhase();

        assertNotEquals(0, velvetDawn.map.spawn.listAllSpawnPoints());
    }

    @Test
    public void test_calculate_full_spawn_half_width() throws Exception {
        var config = new Config();
        var velvetDawn = new VelvetDawn(config);

        // 0 Width
        var spawn = new BorderSpawnMode(velvetDawn, config);
        config.spawn = new SpawnConfig(SpawnConfig.SpawnMode.Boundary, 0, 0);
        assertEquals(1, spawn.calculateSpawnBaseHalfWidth(1));
        assertEquals(1, spawn.calculateSpawnBaseHalfWidth(2));

        // Updating width multiplier
        spawn = new BorderSpawnMode(velvetDawn, config);
        config.spawn = new SpawnConfig(SpawnConfig.SpawnMode.Boundary, 3, 0);
        assertEquals(4, spawn.calculateSpawnBaseHalfWidth(1));
        assertEquals(4, spawn.calculateSpawnBaseHalfWidth(2));

        // Updating width addition
        spawn = new BorderSpawnMode(velvetDawn, config);
        config.spawn = new SpawnConfig(SpawnConfig.SpawnMode.Boundary, 2, 2);
        assertEquals(5, spawn.calculateSpawnBaseHalfWidth(1));
        assertEquals(7, spawn.calculateSpawnBaseHalfWidth(2));

        // Updating neighbour multiplier
        config.spawn = new SpawnConfig(SpawnConfig.SpawnMode.Boundary, 3, 2);
        spawn = new BorderSpawnMode(velvetDawn, config);
        assertEquals(6, spawn.calculateSpawnBaseHalfWidth(1));
        assertEquals(8, spawn.calculateSpawnBaseHalfWidth(2));
    }

    /** Test the correct central spawn ordinates are layed out correct */
    @Test
    public void test_get_central_spawn_ordinates() throws Exception {
        var config = new Config();
        config.map.width = 7;
        config.map.height = 5;
        config.spawn.baseSpawnRadius = 0;
        config.spawn.spawnRadiusMultiplier = 0;

        var spawn = new BorderSpawnMode(new VelvetDawn(config), config);

        var spawns = spawn.getCentralSpawnOrdinates(1, 1);
        assertEquals(1, spawns.size());
        assertTrue(spawns.get(0).tileEquals(new Coordinate(3, 0)));

        spawns = spawn.getCentralSpawnOrdinates(2, 1);
        assertEquals(2, spawns.size());
        assertTrue(spawns.get(0).tileEquals(new Coordinate(3, 0)));
        assertTrue(spawns.get(1).tileEquals(new Coordinate(3, 4)));

        spawns = spawn.getCentralSpawnOrdinates(3, 1);
        assertEquals(3, spawns.size());
        assertTrue(spawns.get(0).tileEquals(new Coordinate(3, 0)));
        assertTrue(spawns.get(1).tileEquals(new Coordinate(6, 3)));
        assertTrue(spawns.get(2).tileEquals(new Coordinate(1, 4)));

        spawns = spawn.getCentralSpawnOrdinates(4, 1);
        assertEquals(4, spawns.size());
        assertTrue(spawns.get(0).tileEquals(new Coordinate(3, 0)));
        assertTrue(spawns.get(1).tileEquals(new Coordinate(6, 2)));
        assertTrue(spawns.get(2).tileEquals(new Coordinate(3, 4)));
        assertTrue(spawns.get(3).tileEquals(new Coordinate(0, 2)));
    }

    /** Test the correct central spawn ordinates are layed out correct with
     more realistic size */
    @Test
    public void test_get_central_spawn_ordinates_with_realistic_values() throws Exception {
        var config = new Config();
        config.map.width = 41;
        config.map.height = 25;
        config.spawn = new SpawnConfig(SpawnConfig.SpawnMode.Boundary, 2, 2);

        var borderSpawn = new BorderSpawnMode(new VelvetDawn(config), config);

        var spawns = borderSpawn.getCentralSpawnOrdinates(1, 2);
        assertTrue(spawns.get(0).tileEquals(new Coordinate(20, 0)));

        spawns = borderSpawn.getCentralSpawnOrdinates(2, 2);
        assertTrue(spawns.get(0).tileEquals(new Coordinate(20, 0)));
        assertTrue(spawns.get(1).tileEquals(new Coordinate(20, 24)));

        spawns = borderSpawn.getCentralSpawnOrdinates(3, 2);
        assertTrue(spawns.get(0).tileEquals(new Coordinate(20, 0)));
        assertTrue(spawns.get(1).tileEquals(new Coordinate(40, 18)));
        assertTrue(spawns.get(2).tileEquals(new Coordinate(8, 24)));

        spawns = borderSpawn.getCentralSpawnOrdinates(4, 2);
        assertTrue(spawns.get(0).tileEquals(new Coordinate(20, 0)));
        assertTrue(spawns.get(1).tileEquals(new Coordinate(40, 12)));
        assertTrue(spawns.get(2).tileEquals(new Coordinate(20, 24)));
        assertTrue(spawns.get(3).tileEquals(new Coordinate(0, 12)));
    }

    /** Test spawning is correct when map is too small */
    @Test
    public void test_get_central_spawn_ordinates_too_small() throws Exception {
        var config = new Config();
        config.map.width = 7;
        config.map.height = 5;
        config.spawn = new SpawnConfig(SpawnConfig.SpawnMode.Boundary, 2, 2);

        var spawn = new BorderSpawnMode(new VelvetDawn(config), config);

        assertThrows(Exception.class, () ->
            spawn.getCentralSpawnOrdinates(1, 1));
    }

    /** Test getting the cell based on the perimeter index */
    @Test
    public void test_get_cell_from_perimeter_index() throws Exception {
        var config_3x3 = new Config();
        config_3x3.map.width = 3;
        config_3x3.map.height = 3;
        var config_4x4 = new Config();
        config_4x4.map.width = 4;
        config_4x4.map.height = 4;
        var borderSpawn3 = new BorderSpawnMode(new VelvetDawn(config_3x3), config_3x3);
        var borderSpawn4 = new BorderSpawnMode(new VelvetDawn(config_4x4), config_4x4);

        var correctPoints = List.of(
                List.of(0, 0),
                List.of(1, 0),
                List.of(2, 0),
                List.of(2, 1),
                List.of(2, 2),
                List.of(1, 2),
                List.of(0, 2),
                List.of(0, 1));
        for (int i = 0; i < 8; i++) {
            var currentPoint = borderSpawn3.getCellFromPerimeterIndex(i);
            assertEquals(currentPoint.x, correctPoints.get(i).get(0), 0);
            assertEquals(currentPoint.y, correctPoints.get(i).get(1), 0);
        }

        correctPoints = List.of(
                List.of(0, 0), List.of(1, 0), List.of(2, 0),
                List.of(3, 0), List.of(3, 1), List.of(3, 2),
                List.of(3, 3), List.of(2, 3), List.of(1, 3),
                List.of(0, 3), List.of(0, 2), List.of(0, 1)
        );
        for (int i = 0; i < 12; i++) {
            var currentPoint = borderSpawn4.getCellFromPerimeterIndex(i);
            assertEquals(currentPoint.x, correctPoints.get(i).get(0), 0);
            assertEquals(currentPoint.y, correctPoints.get(i).get(1), 0);
        }
    }

    /** Test looping around the perimeter gives the next item */
    @Test
    public void test_get_next_coordinate() throws Exception {
        var config_3x3 = new Config();
        config_3x3.map.width = 3;
        config_3x3.map.height = 3;
        var config_4x4 = new Config();
        config_4x4.map.width = 4;
        config_4x4.map.height = 4;
        var borderSpawn3 = new BorderSpawnMode(new VelvetDawn(config_3x3), config_3x3);
        var borderSpawn4 = new BorderSpawnMode(new VelvetDawn(config_4x4), config_4x4);

        // clockwise 3x3
        var correct_points = List.of(List.of(1, 0), List.of(2, 0), List.of(2, 1), List.of(2, 2), List.of(1, 2), List.of(0, 2), List.of(0, 1), List.of(0, 0));
        var current_point = new Coordinate(0, 0);

        for (int i = 0; i < 8; i++) {
            current_point = borderSpawn3.getNextCoordinate(current_point);
            assertEquals(current_point.x, correct_points.get(i).get(0), 0);
            assertEquals(current_point.y, correct_points.get(i).get(1), 0);
        }

        // clockwise 4x4
        correct_points = List.of(
                List.of(1, 0), List.of(2, 0), List.of(3, 0),
                List.of(3, 1), List.of(3, 2), List.of(3, 3),
                List.of(2, 3), List.of(1, 3), List.of(0, 3),
                List.of(0, 2), List.of(0, 1), List.of(0, 0)
        );
        current_point = new Coordinate(0, 0);

        for (int i = 0; i < 12; i++) {
            current_point = borderSpawn4.getNextCoordinate(current_point);
            assertEquals(current_point.x, correct_points.get(i).get(0), 0);
            assertEquals(current_point.y, correct_points.get(i).get(1), 0);
        }
    }
}