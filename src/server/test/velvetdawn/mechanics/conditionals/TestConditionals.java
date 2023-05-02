package velvetdawn.mechanics.conditionals;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.mechanics.conditionals.Comparison;
import velvetdawn.core.mechanics.conditionals.Conditionals;
import velvetdawn.core.mechanics.conditionals.CountConditional;
import velvetdawn.core.mechanics.conditionals.StandardConditional;
import velvetdawn.core.models.anytype.AnyJson;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;


public class TestConditionals extends BaseTest {

    /** Test the various aspect of parsing to make sure the correct errors are raised */
    @Test
    public void test_conditional_parsing() throws Exception {
        var velvetDawn = this.prepareGame();

        // Random key
        assertThrows(Exception.class, () -> Conditionals.get(velvetDawn, "", new AnyJson()
                .set("if", "self")
                .set("fsa", "random key")));

        // Two operations
        assertThrows(Exception.class, () -> Conditionals.get(velvetDawn, "", new AnyJson()
                .set("if", "self")
                .set("gt", 5)
                .set("lt", 5)));

        // Cannot compare greater than to a string
        assertThrows(Exception.class, () -> Conditionals.get(velvetDawn, "", new AnyJson()
                .set("if", "self")
                .set("gt", "5")));

        // Cannot compare tags on an attribute
        assertThrows(Exception.class, () -> Conditionals.get(velvetDawn, "", new AnyJson()
                .set("if", "self.attribute")
                .set("tagged", "atag")));

        // Cannot compare tagged on a count condition
        assertThrows(Exception.class, () -> Conditionals.get(velvetDawn, "", new AnyJson()
                .set("count", "self")
                .set("tagged", "atag")));

        // Test standard comparison
        var conditional = Conditionals.get(velvetDawn, "", new AnyJson()
                .set("if", "self")
                .set("equals", "testing:commander")
                .set("reason", "Instance is not a commander")
                .set("notes", "Test if is a commander"));

        assertEquals("Instance is not a commander", conditional.notTrueReason);
        assertEquals(Comparison.EQUALS, conditional.function);
        assertEquals("testing:commander", conditional.functionValue.rawValue.toString());
        assertTrue(conditional instanceof StandardConditional);

        // Test count
        conditional = Conditionals.get(velvetDawn, "", new AnyJson()
                        .set("count", "entity")
                        .set("equals", 4)
                        .set("reason", "There must be four units")
                        .set("notes", "Test if there are four units"));

        assertEquals("There must be four units", conditional.notTrueReason);
        assertEquals(Comparison.EQUALS, conditional.function);
        assertEquals(4, conditional.functionValue.rawValue.toNumber(), 0);
        assertTrue(conditional instanceof CountConditional);

        // Test invalid key (not if/count)
        assertThrows(Exception.class, () -> Conditionals.get(velvetDawn, "", new AnyJson()
                .set("basic", "entity")
                .set("equals", 4)
                .set("reason", "There must be four units")
                .set("notes", "Test if there are four units")));
    }
}
