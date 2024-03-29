package velvetdawn.mechanics.selectors;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.mechanics.selectors.SelectorEntities;
import velvetdawn.core.mechanics.selectors.SelectorSelf;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyNull;
import velvetdawn.core.models.instances.WorldInstance;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;


public class TestChainedSelectors extends BaseTest {

    @Test
    public void test_selector_parsing() throws Exception {
        var velvetDawn = this.prepareGame();

        // Parsing self selector for both types
        assertTrue(Selectors.get(velvetDawn, "0", "self.health.max") instanceof SelectorSelf);
        var selector = Selectors.get(
                velvetDawn,
                "0",
                "entities>entities[range=2]>entities[commander].health");
        assertTrue(selector instanceof SelectorEntities);
        assertTrue(selector.chainedSelector instanceof SelectorEntities);
        assertTrue(selector.chainedSelector.chainedSelector instanceof SelectorEntities);
        assertEquals(selector.attribute, "health");
        assertEquals(selector.chainedSelector.filters.maxRange, 2, 0);
    }

    @Test
    public void test_attributes() throws Exception {
        var velvetDawn = this.prepareGame();

        assertEquals(Selectors.get(velvetDawn, "0", "self.health.max").attribute, "health.max");
        assertEquals(Selectors.get(velvetDawn, "0", "entities[id=1].combat.range").attribute, "combat.range");
        assertNull(Selectors.get(velvetDawn, "0", "tile").attribute);
    }

    /** Test get values handles different data types properly */
    @Test
    public void test_selector_get_value() throws Exception {
        var velvetDawn = this.prepareGame();

        var entities = velvetDawn.entities.list();

        // No attributes on units, so returns none
        assertTrue(Selectors.get(velvetDawn, "0", "entities.example")
                .funcGetValue(WorldInstance.getInstance()) instanceof AnyNull);

        // Test with one number
        entities.get(0).attributes.set("example", Any.from(5));
        assertEquals(5, Selectors.get(velvetDawn, "0", "entities.example")
                .funcGetValue(WorldInstance.getInstance()).toNumber(), 0);

        // Test the average of the two numbers
        entities.get(1).attributes.set("example", Any.from(3));
        assertEquals(4, Selectors.get(velvetDawn, "0", "entities.example")
                .funcGetValue(WorldInstance.getInstance()).toNumber(), 0);

        // Test mixed values
        entities.get(1).attributes.set("example", Any.from("dsadsa"));
        assertTrue(Selectors.get(velvetDawn, "0", "entities.example")
                .funcGetValue(WorldInstance.getInstance()) instanceof AnyNull);

        // Test not equal strings
        entities.get(0).attributes.set("example", Any.from("dsadsa"));
        entities.get(1).attributes.set("example", Any.from("aaaaa"));
        assertTrue(Selectors.get(velvetDawn, "0", "entities.example")
                .funcGetValue(WorldInstance.getInstance()) instanceof AnyNull);

        // Test equal strings
        entities.get(0).attributes.set("example", Any.from("aaaaa"));
        entities.get(1).attributes.set("example", Any.from("aaaaa"));
        assertEquals("aaaaa", Selectors.get(velvetDawn,"0", "entities.example")
                .funcGetValue(WorldInstance.getInstance()).toString());
    }
}
