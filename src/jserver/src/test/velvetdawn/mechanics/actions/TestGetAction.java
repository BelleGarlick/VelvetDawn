package test.velvetdawn.mechanics.actions;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.mechanics.actions.ActionModify;
import velvetdawn.mechanics.actions.Actions;
import velvetdawn.models.Coordinate;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.anytype.AnyList;
import velvetdawn.models.instances.entities.EntityInstance;

import java.util.List;

import static junit.framework.TestCase.*;
import static org.junit.Assert.assertThrows;


public class TestGetAction extends BaseTest {

    @Test
    public void testGetActions() throws Exception {
        var velvetDawn = this.prepareGame();

        var action = Actions.fromJson(velvetDawn, "0", new AnyJson()
                .set("modify", "self.health")
                .set("set", "x"));

        assertTrue(action instanceof ActionModify);

        // Invalid action
        assertThrows(Exception.class, () -> {
            Actions.fromJson(velvetDawn, "0", new AnyJson().set("random key", "self.health"));
        });
    }

    @Test
    public void testActioCanRun() throws Exception {
        var velvetDawn = this.prepareGame();

        EntityInstance unit = velvetDawn.entities.getAtPosition(new Coordinate(5, 0)).get(0);
        var action = Actions.fromJson(velvetDawn, "0", new AnyJson()
                .set("modify", "self.health")
                .set("set", 100)
                .set("conditions", AnyList.of(
                        new AnyJson()
                                .set("if", "self.health")
                                .set("lte", 10)
                )));

        unit.attributes.set("health", Any.from(50));
        assertFalse(action.canRun(unit));

        unit.attributes.set("health", Any.from(2));
        assertTrue(action.canRun(unit));
    }
}

