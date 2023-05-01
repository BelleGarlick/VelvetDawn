package test.velvetdawn.mechanics.selectors;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.mechanics.selectors.SelectorEntities;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.mechanics.selectors.WorldSelector;
import velvetdawn.core.mechanics.selectors.closest.SelectorClosest;
import velvetdawn.core.models.Coordinate;

import java.util.ArrayList;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;


public class TestSelectors extends BaseTest {

    @Test
    public void test_selector_parsing() throws Exception {
        var selector = Selectors.get(this.prepareGame(), "0", "world>entities[commander]>closest.max.health.example");

        assertTrue(selector instanceof WorldSelector);
        assertTrue(selector.chainedSelector instanceof SelectorEntities);
        assertTrue(selector.chainedSelector.chainedSelector instanceof SelectorClosest);

        assertEquals(selector.attribute, "max.health.example");
    }

    @Test
    public void test_chained_selectors() throws Exception {
        var velvetDawn = this.prepareGame();

        var selector = Selectors.get(velvetDawn, "", "world>entities[commander]>tile.max.health.example");

        var tiles = selector.getChainedSelection(new ArrayList<>(
                velvetDawn.entities.getAtPosition(new Coordinate(5, 0))).get(0));

        // 3 units with two commanders each on 1 tile results in 2 tiles
        assertEquals(2, tiles.size());
    }
}
