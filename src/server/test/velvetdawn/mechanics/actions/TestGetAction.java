package velvetdawn.mechanics.actions;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.mechanics.actions.ActionModify;
import velvetdawn.core.mechanics.actions.Actions;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;
import velvetdawn.core.entities.EntityInstance;

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

