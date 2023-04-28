package test.velvetdawn;

import static org.junit.Assert.*;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.Phase;
import velvetdawn.models.config.Config;


public class TestSetup extends BaseTest {

    @Test
    public void test_updating_setup_definition() throws Exception {
        Config config = this.getConfig();
        VelvetDawn velvetDawn = new VelvetDawn(config);

        var p1 = velvetDawn.players.join("player1", "null");
        
        var setup = velvetDawn.game.setup.getSetup(p1);
        assertTrue(setup.getCommanders().isEmpty());
        assertTrue(setup.getEntities().isEmpty());
        
        assertThrows(Exception.class, () -> {
            velvetDawn.game.setup.updateSetup("invalid_name", 10);
        });

        // Add item to setup
        velvetDawn.game.setup.updateSetup("testing:abilitied", 10);
        setup = velvetDawn.game.setup.getSetup(p1);
        assertEquals(10, setup.getEntities().get("testing:abilitied").intValue());

        // Remove item from setup
        velvetDawn.game.setup.updateSetup("testing:abilitied", 0);
        setup = velvetDawn.game.setup.getSetup(p1);
        assertTrue(setup.getEntities().isEmpty());

        // Add commanders
        velvetDawn.game.setup.updateSetup("testing:commander", 10);
        setup = velvetDawn.game.setup.getSetup(p1);
        assertEquals(1, setup.getCommanders().size());

        // Test setup is valid with commanders
        velvetDawn.game.setup.updateSetup("testing:abilitied", 1);
        assertTrue(velvetDawn.game.setup.isSetupValid());

        // Test invalid setup with no commanders but has entities
        velvetDawn.game.setup.updateSetup("testing:commander", 0);
        assertFalse(velvetDawn.game.setup.isSetupValid());
    }

    @Test
    public void test_place_setup_entity() throws Exception {
        Config config = this.getTestConfig();
        VelvetDawn velvetDawn = new VelvetDawn(config);

        velvetDawn.game.phase = Phase.Lobby;

        var p1 = velvetDawn.players.join("player1", "null");
        var p2 = velvetDawn.players.join("player2", "null");

        velvetDawn.map.generate();
        velvetDawn.game.startSetupPhase();

        // Test random entity throws error
        assertThrows(Exception.class, () -> {
            velvetDawn.game.setup.placeEntity(p1, "dsjakdksla", new Coordinate(0, 0));
        });

        // Test trying to place a commander and entity not in the setup definition
        assertThrows(Exception.class, () -> {
            velvetDawn.game.setup.placeEntity(p1, "civil-war:commander",  new Coordinate(14, 0));
        });
        assertThrows(Exception.class, () -> {
            velvetDawn.game.setup.placeEntity(p1, "civil-war:musketeers",  new Coordinate(14, 0));
        });

        // Update the setup definition to allow a commander and two muskets
        velvetDawn.game.phase = Phase.Lobby;
        velvetDawn.game.setup.updateSetup("civil-war:commander", 1);
        velvetDawn.game.setup.updateSetup("civil-war:musketeers", 2);
        velvetDawn.game.phase = Phase.Setup;

        // Test creating twos commander is an issue and that a commander can be removed and re-added
        // also testing that removing an entity with no entity to remove will raise an error
        velvetDawn.game.setup.placeEntity(p1, "civil-war:commander", new Coordinate(14, 0));
        assertThrows(Exception.class, () -> velvetDawn.game.setup.placeEntity(p1, "civil-war:commander", new Coordinate(15, 0)));
        assertThrows(Exception.class, () -> velvetDawn.game.setup.removeEntity(p1, new Coordinate(15, 0)));
        velvetDawn.game.setup.removeEntity(p1, new Coordinate(14, 0));
        velvetDawn.game.setup.placeEntity(p1, "civil-war:commander", new Coordinate(15, 0));

        // Test placing and placing in same pos and placing too many
        velvetDawn.game.setup.placeEntity(p1, "civil-war:musketeers", new Coordinate(14, 1));
        // Placing two items in same cell
        assertThrows(Exception.class, () -> {
            velvetDawn.game.setup.placeEntity(p1, "civil-war:musketeers", new Coordinate(14, 1));
        });
        velvetDawn.game.setup.placeEntity(p1, "civil-war:musketeers", new Coordinate(13, 0));

        // too many places
        assertThrows(Exception.class, () -> {
            velvetDawn.game.setup.placeEntity(p1, "civil-war:musketeers", new Coordinate(14, 2));
        });

        // Test is not validated until player b has been setup
        assertFalse(velvetDawn.game.setup.validatePlayerSetups());

        velvetDawn.game.setup.placeEntity(p2, "civil-war:musketeers", new Coordinate(14, 17));
        velvetDawn.game.setup.placeEntity(p2, "civil-war:musketeers", new Coordinate(15, 17));
        velvetDawn.game.setup.placeEntity(p2, "civil-war:commander", new Coordinate(13, 17));

        assertTrue(velvetDawn.game.setup.validatePlayerSetups());
    }
}
