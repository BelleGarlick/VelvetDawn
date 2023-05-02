package test.velvetdawn.mechanics.conditionals;

import org.junit.Test;
import velvetdawn.core.mechanics.conditionals.Conditionals;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.instances.entities.EntityInstance;

import static junit.framework.TestCase.assertFalse;
import static org.junit.Assert.assertThrows;
import static org.junit.Assert.assertTrue;

public class TestConditionalIf extends test.BaseTest {

    @Test
    public void test_conditional_if() throws Exception {
        var velvetDawn = this.prepareGame();

        EntityInstance entity = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);

        var conditionalEquals = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.testing")
                .set("equals", 5));
        var conditionalNotEquals = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.testing")
                .set("ne", 5));
        var conditionalLessThan = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.testing")
                .set("lt", 5));
        var conditionalLessThanEquals = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.testing")
                .set("lte", 5));
        var conditionalGreaterThan = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.testing")
                .set("gt", 5));
        var conditionalGreaterThanEquals = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.testing")
                .set("gte", 5));
        var conditionalHasTag = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self")
                .set("tagged", "x"));

        // cant compare tag on attribute
        assertThrows(Exception.class, () -> Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.testing")
                .set("tagged", "x")));

        assertFalse(conditionalEquals.isTrue(entity));

        entity.attributes.set("testing", Any.from(5));

        assertTrue(conditionalEquals.isTrue(entity));
        assertFalse(conditionalNotEquals.isTrue(entity));
        assertFalse(conditionalLessThan.isTrue(entity));
        assertTrue(conditionalLessThanEquals.isTrue(entity));
        assertFalse(conditionalGreaterThan.isTrue(entity));
        assertTrue(conditionalGreaterThanEquals.isTrue(entity));
        assertFalse(conditionalHasTag.isTrue(entity));

        entity.tags.add("x");

        assertTrue(conditionalHasTag.isTrue(entity));
    }

    @Test
    public void test_conditional_if_function_value() throws Exception {
        var velvetDawn = this.prepareGame();

        EntityInstance entity = velvetDawn.entities.list().get(0);
        entity.attributes.set("example1", Any.from(5));
        entity.attributes.set("example2", Any.from(5));
        entity.attributes.set("example3", Any.from(3));

        var conditional_equals = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.example1")
                .set("equals", "@self.example2"));
        var conditional_not_equals = Conditionals.get(velvetDawn, "0", new AnyJson()
                .set("if", "self.example1")
                .set("equals", "@self.example3"));

        assertTrue(conditional_equals.isTrue(entity));
        assertFalse(conditional_not_equals.isTrue(entity));
    }
}
