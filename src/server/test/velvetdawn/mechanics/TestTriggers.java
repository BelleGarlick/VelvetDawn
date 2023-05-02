package velvetdawn.mechanics;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.VelvetDawn;
import velvetdawn.core.mechanics.actions.Actions;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.instances.WorldInstance;
import velvetdawn.core.entities.EntityInstance;

import java.util.List;

import static junit.framework.TestCase.assertFalse;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;
import static org.junit.Assert.assertTrue;


/** Test all triggers are executed correctly

Units and tiles will be assigned a trigger then
a test is performed to check that trigger was
executed.
*/


// TODO Finish tests here when targeting and combat is complete


public class TestTriggers extends BaseTest {

    /** Assign a trigger on the given trigger name */
    public void set_commander_trigger(VelvetDawn velvetDawn, String triggerName) throws Exception {
        velvetDawn.datapacks.entities.get("testing:commander").triggers.triggers.put(triggerName, List.of(
                Actions.fromJson(velvetDawn, "", new AnyJson()
                        .set("modify", "self.health")
                        .set("set", 0.1f))
        ));
    }

    private EntityInstance getPlayerCommander(VelvetDawn velvetDawn, int playerNumber) {
        return velvetDawn.entities.list()
                .stream()
                .filter(x -> x.datapackId.equals("testing:commander") && x.player.name.equals(String.format("player%s", playerNumber)))
                .findFirst()
                .orElse(null);
    }
    
    /** Assign a trigger to a tile on the given trigger name */
    public void set_commander_tile_trigger(VelvetDawn velvetDawn, String triggerName) throws Exception {
        velvetDawn.datapacks.entities.get("testing:commander").triggers.triggers.put(triggerName, List.of(
                Actions.fromJson(velvetDawn, "", new AnyJson()
                        .set("modify", "tile.test")
                        .set("set", 0.1f))
        ));
    }
    
    @Test
    public void test_trigger_turn() throws Exception {
        var velvetDawn = this.prepareGame();

        set_commander_trigger(velvetDawn, "turn");
        WorldInstance.getInstance().tags.remove("turn-trigger-ran");

        var commander = this.getPlayerCommander(velvetDawn, 1);
        assertNotEquals(0.1, commander.attributes.get("health").toNumber());

        // Begin turn should trigger the health update
        velvetDawn.game.turns.beginNextTurn();

        assertEquals(0.1, commander.attributes.get("health").toNumber(), 0.0001);
        assertTrue(WorldInstance.getInstance().tags.contains("turn-trigger-ran"));
    }

    @Test
    public void test_trigger_turn_end() throws Exception {
        var velvetDawn = this.prepareGame();

        set_commander_trigger(velvetDawn, "turn-end");
        WorldInstance.getInstance().tags.remove("turn-end-trigger-ran");

        var commander = this.getPlayerCommander(velvetDawn, 1);
        assertNotEquals(0.1, commander.attributes.get("health").toNumber());

        // On turn end will update the health
        velvetDawn.game.turns.beginNextTurn();

        assertEquals(0.1, commander.attributes.get("health").toNumber(), 0.001);
        assertTrue(WorldInstance.getInstance().tags.contains("turn-end-trigger-ran"));
    }
            
    @Test
    public void test_trigger_friendly_turn() throws Exception {
        var velvetDawn = this.setupGame();
        set_commander_trigger(velvetDawn, "friendly-turn");

        var player_a_commander = getPlayerCommander(velvetDawn, 1);
        var player_b_commander = getPlayerCommander(velvetDawn, 2);

        assertNotEquals(0.1, player_a_commander.attributes.get("health"));
        assertNotEquals(0.1, player_b_commander.attributes.get("health"));

        // On turn end will start player_b"s turn so player_a will not update
        velvetDawn.game.turns.beginNextTurn();

        assertNotEquals(0.1, player_a_commander.attributes.get("health").toNumber());
        assertEquals(0.1, player_b_commander.attributes.get("health").toNumber(), 0.001);

        // Back to player a
        velvetDawn.game.turns.beginNextTurn();

        assertEquals(0.1, player_a_commander.attributes.get("health").toNumber(), 0.001);
        assertEquals(0.1, player_b_commander.attributes.get("health").toNumber(), 0.001);
    }

    @Test
    public void testTriggerFriendlyTurnEnd() throws Exception {
        var velvetDawn = this.setupGame();
        set_commander_trigger(velvetDawn, "friendly-turn-end");

        var player_a_commander = getPlayerCommander(velvetDawn, 1);
        var player_b_commander = getPlayerCommander(velvetDawn, 2);

        assertNotEquals(0.1, player_a_commander.attributes.get("health"));
        assertNotEquals(0.1, player_b_commander.attributes.get("health"));

        // On turn end will end player_a"s turn so player_b will not update
        velvetDawn.game.turns.beginNextTurn();

        assertEquals(0.1, player_a_commander.attributes.get("health").toNumber(), 0.001);
        assertNotEquals(0.1, player_b_commander.attributes.get("health"));

        // End player_b
        velvetDawn.game.turns.beginNextTurn();

        assertEquals(0.1, player_a_commander.attributes.get("health").toNumber(), 0.001);
        assertEquals(0.1, player_b_commander.attributes.get("health").toNumber(), 0.001);
    }

    @Test
    public void test_trigger_enemy_turn() throws Exception {
        var velvetDawn = this.setupGame();
        set_commander_trigger(velvetDawn, "enemy-turn");

        var player_a_commander = getPlayerCommander(velvetDawn, 1);
        var player_b_commander = getPlayerCommander(velvetDawn, 2);

        assertNotEquals(0.1, player_a_commander.attributes.get("health").toNumber());
        assertNotEquals(0.1, player_b_commander.attributes.get("health").toNumber());

        // On turn end will start player_b"s so player_a"s (enemy turn) will begin
        velvetDawn.game.turns.beginNextTurn();

        assertEquals(0.1, player_a_commander.attributes.get("health").toNumber(), 0.001);
        assertNotEquals(0.1, player_b_commander.attributes.get("health").toNumber());

        // Back to player a
        velvetDawn.game.turns.beginNextTurn();

        assertEquals(0.1, player_a_commander.attributes.get("health").toNumber(), 0.001);
        assertEquals(0.1, player_b_commander.attributes.get("health").toNumber(), 0.001);
    }

    @Test
    public void test_trigger_enemy_turn_end() throws Exception {
        var velvetDawn = this.setupGame();
        set_commander_trigger(velvetDawn, "enemy-turn-end");

        var player_a_commander = getPlayerCommander(velvetDawn, 1);
        var player_b_commander = getPlayerCommander(velvetDawn, 2);

        assertNotEquals(0.1, player_a_commander.attributes.get("health").toNumber());
        assertNotEquals(0.1, player_b_commander.attributes.get("health").toNumber());

        // On turn end will end player_a"s so player_b"s (enemy turn) will end
        velvetDawn.game.turns.beginNextTurn();

        assertNotEquals(0.1, player_a_commander.attributes.get("health").toNumber());
        assertEquals(0.1, player_b_commander.attributes.get("health").toNumber(), 0.001);

        // End player_b
        velvetDawn.game.turns.beginNextTurn();

        assertEquals(0.1, player_a_commander.attributes.get("health").toNumber(), 0.001);
        assertEquals(0.1, player_b_commander.attributes.get("health").toNumber(), 0.001);
    }

    @Test
    public void test_trigger_enter() throws Exception {
        var velvetDawn = this.prepareGame();
        set_commander_tile_trigger(velvetDawn, "enter");

        var commander = this.getPlayerCommander(velvetDawn, 1);

        var instance = velvetDawn.entities.movement.move(commander, List.of(
                new Coordinate(commander.position.x, commander.position.y),
                new Coordinate(commander.position.x, commander.position.y + 1)
        ));

        var newTile = velvetDawn.map.getTile(instance.position);
        assertEquals(0.1, newTile.attributes.get("test").toNumber(), 0.001);
    }

    @Test
    public void test_trigger_leave() throws Exception {
        var velvetDawn = this.prepareGame();
        set_commander_tile_trigger(velvetDawn, "leave");

        var commander = this.getPlayerCommander(velvetDawn, 1);

        velvetDawn.entities.movement.move(commander, List.of(
                commander.position,
                commander.position.down()
        ));

        var new_tile = velvetDawn.map.getTile(commander.position.up());
        assertEquals(0.1, new_tile.attributes.get("test").toNumber(), 0.001);
    }

    @Test
    public void test_trigger_spawn() throws Exception {
        var config = this.getTestConfig();
        config.seed = 0;
        var velvetDawn = new VelvetDawn(config);

        set_commander_trigger(velvetDawn, "spawn");

        var player = velvetDawn.players.join("player1", "");
        velvetDawn.players.join("player2", "");
        velvetDawn.game.setup.updateSetup("testing:commander", 1);
        velvetDawn.game.startSetupPhase();
        velvetDawn.game.setup.placeEntity(player, "testing:commander", new Coordinate(15, 0));

        var commander = getPlayerCommander(velvetDawn, 1);
        assertEquals(0.1, commander.attributes.get("health").toNumber(), 0.001);
    }

    @Test
    public void test_trigger_game_begin() throws Exception {
        var config = this.getConfig();
        config.seed = 0;

        var velvetDawn = new VelvetDawn(config);

        set_commander_trigger(velvetDawn, "game");

        var player1 = velvetDawn.players.join("player1", "");
        velvetDawn.players.join("player2", "");
        velvetDawn.game.setup.updateSetup("testing:commander", 1);
        velvetDawn.game.startSetupPhase();
        velvetDawn.game.setup.placeEntity(player1, "testing:commander", new Coordinate(6, 0));
        velvetDawn.game.startGamePhase();

        var commander = velvetDawn.entities.list().get(0);
        assertEquals(0.1, commander.attributes.get("health").toNumber(), 0.001);
        assertTrue(WorldInstance.getInstance().tags.contains("game-trigger-ran"));
    }
            
    @Test
    public void test_trigger_round_begin() throws Exception {
        var velvetDawn = this.prepareGame();
        WorldInstance.getInstance().tags.remove("round-trigger-ran");

        velvetDawn.game.turns.beginNextTurn();
        assertFalse(WorldInstance.getInstance().tags.contains("round-trigger-ran"));

        velvetDawn.game.turns.beginNextTurn();
        assertTrue(WorldInstance.getInstance().tags.contains("round-trigger-ran"));
    }

    // public void test_trigger_death(self):
    //     with app.app_context():
    //         assertTrue(False)
    //
    // public void test_trigger_kill(self):
    //     with app.app_context():
    //         assertTrue(False)
    //
    // public void test_trigger_attack(self):
    //     with app.app_context():
    //         assertTrue(False)
    //
    // public void test_trigger_attacked(self):
    //     with app.app_context():
    //         assertTrue(False)

    // public void test_trigger_target(self):
    //     with app.app_context():
    //         assertTrue(False)
    //
    // public void test_trigger_targeted(self):
    //     with app.app_context():
    //         assertTrue(False)
}