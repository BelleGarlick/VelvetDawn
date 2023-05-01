package test.velvetdawn.mechanics.selectors;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.instances.WorldInstance;

import java.util.ArrayList;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;


public class TestSelfSelector extends BaseTest {

    @Test
    public void test_selector_self() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);
        var tile = velvetDawn.map.getTile(new Coordinate(5, 0));

        var selector = Selectors.get(velvetDawn, "", "self");

        assertEquals(unit.instanceId, new ArrayList<>(selector.getChainedSelection(unit)).get(0).instanceId);
        assertEquals(tile.instanceId, new ArrayList<>(selector.getChainedSelection(tile)).get(0).instanceId);

        assertSame(
                WorldInstance.getInstance(),
                new ArrayList<>(selector.getChainedSelection(WorldInstance.getInstance())).get(0));
    }
}
