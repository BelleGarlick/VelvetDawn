package test.velvetdawn.map;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.config.Config;

import java.util.List;

import static junit.framework.TestCase.assertFalse;
import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;

public class TestMapCreation extends BaseTest {

    @Test
    public void test_map_creation() throws Exception {
        var config = new Config();
        config.map.height = 20;
        config.map.width = 20;
        config.seed = 79221;
        config.datapacks = List.of("civil-war");

        var velvetDawn = new VelvetDawn(config);
        velvetDawn.players.join("acdc", "");

        velvetDawn.map.generate();
    }
}