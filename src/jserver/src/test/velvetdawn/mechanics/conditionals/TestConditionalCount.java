package test.velvetdawn.mechanics.conditionals;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.mechanics.conditionals.Conditionals;
import velvetdawn.models.Coordinate;
import velvetdawn.models.anytype.Any;
import velvetdawn.utils.Json;

import java.util.ArrayList;

import static junit.framework.TestCase.assertFalse;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

public class TestConditionalCount extends BaseTest {

    @Test
    public void test_conditional_count() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);

        var conditionalEquals = Conditionals.get(velvetDawn, "0", new Json()
                .set("count", "entities")
                .set("equals", 4));
        var conditionalNotEquals = Conditionals.get(velvetDawn, "0", new Json()
                .set("count", "entities")
                .set("ne", 4));
        var conditionalLessThan = Conditionals.get(velvetDawn, "0", new Json()
                .set("count", "entities")
                .set("lt", 4));
        var conditionalLessThanEquals = Conditionals.get(velvetDawn, "0", new Json()
                .set("count", "entities")
                .set("lte", 4));
        var conditionalGreaterThan = Conditionals.get(velvetDawn, "0", new Json()
                .set("count", "entities")
                .set("gt", 4));
        var conditionalGreaterThanEquals = Conditionals.get(velvetDawn, "0", new Json()
                .set("count", "entities")
                .set("gte", 4));

        // can't compare tag on attribute
        assertThrows(Exception.class, () -> Conditionals.get(velvetDawn, "", new Json()
                .set("count", "self")
                .set("tagged", "atag")));

        assertTrue(conditionalEquals.isTrue(unit));
        assertFalse(conditionalNotEquals.isTrue(unit));
        assertFalse(conditionalLessThan.isTrue(unit));
        assertTrue(conditionalLessThanEquals.isTrue(unit));
        assertFalse(conditionalGreaterThan.isTrue(unit));
        assertTrue(conditionalGreaterThanEquals.isTrue(unit));
    }

    @Test
    public void test_conditional_if_function_value() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = new ArrayList<>(velvetDawn.entities.list()).get(0);
        unit.attributes.set("units-count-true", Any.from(4));
        unit.attributes.set("units-count-false", Any.from(5));

        var conditionalEquals = Conditionals.get(velvetDawn, "", new Json()
                .set("count", "entities")
                .set("equals", "@self.units-count-true"));
        var conditionalNotEquals = Conditionals.get(velvetDawn, "", new Json()
                .set("count", "entities")
                .set("equals", "@self.units-count-false"));

        assertTrue(conditionalEquals.isTrue(unit));
        assertFalse(conditionalNotEquals.isTrue(unit));
    }
}
