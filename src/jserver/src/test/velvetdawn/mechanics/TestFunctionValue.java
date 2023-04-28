package test.velvetdawn.mechanics;

import static org.junit.Assert.*;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.mechanics.FunctionValue;
import velvetdawn.mechanics.selectors.Selector;
import velvetdawn.models.anytype.Any;

import java.util.ArrayList;


public class TestFunctionValue extends BaseTest {

    /*
    Test the FunctionValue works across raw values, selectors
    and random values.
    */

    @Test
    public void test_function_value() throws Exception {
        var velvetDawn = this.prepareGame();

        assertEquals(4, new FunctionValue(velvetDawn, "", Any.from(4))
                .value(null).toNumber(), 0);

        assertEquals("test", new FunctionValue(velvetDawn, "", Any.from("test"))
                .value(null).toString());

        assertNull(new FunctionValue(velvetDawn, "0", Any.Null()).value(null).toString());
        assertTrue(1 >= new FunctionValue(velvetDawn, "0", Any.from("__rand__")).value(null).toNumber());
        assertNotEquals(
                new FunctionValue(velvetDawn, "0", Any.from("__rand__")).value(null).toNumber(),
                new FunctionValue(velvetDawn, "0", Any.from("__rand__")).value(null).toNumber()
        );

        var entity = velvetDawn.entities.list().get(0);
        var function = new FunctionValue(velvetDawn, "0", Any.from("@self"));
        assertTrue(function.selectorValue instanceof Selector);
        assertEquals(entity.datapackId, function.value(entity).toString());

        entity.attributes.set("example", Any.from(5));
        assertEquals(5, new FunctionValue(velvetDawn, "0", Any.from("@self.example")).value(entity).toNumber(), 0);
    }
}
