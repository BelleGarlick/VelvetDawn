package test.velvetdawn.mechanics.selectors;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.mechanics.selectors.closest.SelectorClosest;
import velvetdawn.core.mechanics.selectors.closest.SelectorClosestEnemy;
import velvetdawn.core.mechanics.selectors.closest.SelectorClosestFriendly;
import velvetdawn.core.models.Coordinate;

import java.util.ArrayList;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;


public class TestClosestSelector extends BaseTest {

    // TODO turn closest into a filter not a selector

    @Test
    public void test_selector_parsing() throws Exception {
        var velvetDawn = this.prepareGame();

        var selector_closest_unit = Selectors.get(velvetDawn, "0", "closest");
        var selector_closest_enemy = Selectors.get(velvetDawn, "0", "closest-enemy");
        var selector_closest_friendly = Selectors.get(velvetDawn, "0", "closest-friendly");

        assertTrue(selector_closest_unit instanceof SelectorClosest);
        assertTrue(selector_closest_enemy instanceof SelectorClosestEnemy);
        assertTrue(selector_closest_friendly instanceof SelectorClosestFriendly);
    }

    @Test
    public void test_selector_unit() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);

        var selectorClosestUnit = Selectors.get(velvetDawn, "0", "closest");
        var selectorClosestEnemy = Selectors.get(velvetDawn, "0", "closest-enemy");
        var selectorClosestFriendly = Selectors.get(velvetDawn, "0", "closest-friendly");

        var closest_unit = selectorClosestUnit.getChainedSelection(unit);
        var closest_enemy = selectorClosestEnemy.getChainedSelection(unit);
        var closest_friendly = selectorClosestFriendly.getChainedSelection(unit);

        assertEquals(1, closest_unit.size());
        assertEquals(1, closest_enemy.size());
        assertEquals(1, closest_friendly.size());

        // Test that self is excluded
        assertNotEquals(new ArrayList<>(closest_unit).get(0).instanceId, unit.instanceId);
    }
}