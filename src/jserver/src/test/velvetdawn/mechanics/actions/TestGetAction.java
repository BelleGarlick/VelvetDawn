package test.velvetdawn.mechanics.actions;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.mechanics.actions.ActionModify;
import velvetdawn.mechanics.actions.Actions;
import velvetdawn.models.Coordinate;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.instances.EntityInstance;
import velvetdawn.utils.Json;

import java.util.List;

import static junit.framework.TestCase.*;
import static org.junit.Assert.assertThrows;


public class TestGetAction extends BaseTest {

    @Test
    public void test_get_actions() throws Exception {
        var velvetDawn = this.prepareGame();

        var action = Actions.fromJson(velvetDawn, "0", new Json()
                .set("modify", "self.health")
                .set("set", "x"));

        assertTrue(action instanceof ActionModify);

        // Invalid action
        assertThrows(Exception.class, () -> {
            Actions.fromJson(velvetDawn, "0", new Json().set("random key", "self.health"));
        });
    }

    @Test
    public void test_action_can_run() throws Exception {
        var velvetDawn = this.prepareGame();

        EntityInstance unit = velvetDawn.entities.getAtPosition(new Coordinate(0, -11)).get(0);
        var action = Actions.fromJson(velvetDawn, "0", new Json()
                .set("modify", "self.health")
                .set("set", 100)
                .set("conditions", List.of(
                        new Json()
                                .set("if", "self.health")
                                .set("lte", 10)
                )));

        unit.attributes.set("health", Any.from(50));
        assertFalse(action.canRun(unit));

        unit.attributes.set("health", Any.from(2));
        assertTrue(action.canRun(unit));
    }
}

