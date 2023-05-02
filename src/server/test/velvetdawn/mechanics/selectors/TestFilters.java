package velvetdawn.mechanics.selectors;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.mechanics.selectors.SelectorUnit;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.instances.WorldInstance;

import java.util.ArrayList;

import static junit.framework.TestCase.assertFalse;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;


public class TestFilters extends BaseTest {

    @Test
    public void test_filter_parsing() throws Exception {
        var velvetDawn = this.prepareGame();

        // Test selectors work
        var selector = Selectors.get(
                velvetDawn,
                "0",
                "entity[id=10,tag=dsa,range=100]>entities[commander,id=4,tag=10]");

        assertTrue(selector instanceof SelectorUnit);

        assertTrue(selector.filters.allowedIds.contains("10"));
        assertTrue(selector.filters.allowedTags.contains("dsa"));
        assertFalse(selector.filters.commanderOnly);
        assertEquals(100, selector.filters.maxRange, 0);
        assertNull(selector.filters.minRange);

        assertTrue(selector.chainedSelector.filters.allowedIds.contains("4"));
        assertTrue(selector.chainedSelector.filters.allowedTags.contains("10"));
        assertTrue(selector.chainedSelector.filters.commanderOnly);
        assertNull(selector.chainedSelector.filters.maxRange);
        assertNull(selector.chainedSelector.filters.minRange);
    }

    @Test
    public void test_filters_id() throws Exception {
        var velvetDawn = this.prepareGame();

        var selector_1 = Selectors.get(velvetDawn, "world", "entities[tag=test-tag1]");
        var selector_2 = Selectors.get(velvetDawn, "world", "entities[tag=x]");

        assertEquals(2, selector_1.getChainedSelection(WorldInstance.getInstance()).size());
        assertEquals(0, selector_2.getChainedSelection(WorldInstance.getInstance()).size());
    }

    @Test
    public void test_filters_tags() throws Exception {
        var velvetDawn = this.prepareGame();

        var selector_1 = Selectors.get(velvetDawn, "world", "entities[id=testing:commander]");
        var selector_2 = Selectors.get(velvetDawn, "world", "entities[id=testing:upgradable]");
        var selector_3 = Selectors.get(velvetDawn, "world", "entities[id=testing:commander, id=testing:upgradable]");

        assertEquals(2, selector_1.getChainedSelection(WorldInstance.getInstance()).size());
        assertEquals(1, selector_2.getChainedSelection(WorldInstance.getInstance()).size());
        assertEquals(3, selector_3.getChainedSelection(WorldInstance.getInstance()).size());
    }

    @Test
    public void test_filters_max_range() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);

        var selector_range_0 = Selectors.get(velvetDawn, unit.instanceId, "tiles[range=0]");
        var selector_range_1 = Selectors.get(velvetDawn, unit.instanceId, "tiles[range=1]");
        var selector_range_2 = Selectors.get(velvetDawn, unit.instanceId, "tiles[range=2]");

        assertEquals(1, selector_range_0.getChainedSelection(unit).size());
        assertEquals(6, selector_range_1.getChainedSelection(unit).size());
        assertEquals(13, selector_range_2.getChainedSelection(unit).size());
    }

    @Test
    public void test_filters_min_range() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);

        var selector_range_0 = Selectors.get(velvetDawn, unit.datapackId, "tiles[min-range=0]");
        var selector_range_1 = Selectors.get(velvetDawn, unit.datapackId, "tiles[min-range=1]");
        var selector_range_2 = Selectors.get(velvetDawn, unit.datapackId, "tiles[min-range=2]");

        assertEquals(121, selector_range_0.getChainedSelection(unit).size());
        assertEquals(120, selector_range_1.getChainedSelection(unit).size());
        assertEquals(115, selector_range_2.getChainedSelection(unit).size());
    }

    @Test
    public void test_exclude_test_filter() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);

        var selector_self = Selectors.get(velvetDawn, unit.datapackId, "self[exclude-self]");
        var selector_units = Selectors.get(velvetDawn, unit.datapackId, "entities[exclude-self]");

        assertEquals(0, selector_self.getChainedSelection(unit).size());
        assertEquals(3, selector_units.getChainedSelection(unit).size());  // only 3 of 4 units returned
    }

    @Test
    public void test_selector_unit() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);

        var selectorClosestUnit = Selectors.get(velvetDawn, "0", "entities[closest]");
        var selectorClosestEnemy = Selectors.get(velvetDawn, "0", "enemies[closest]");
        var selectorClosestFriendly = Selectors.get(velvetDawn, "0", "friendlies[closest]");

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