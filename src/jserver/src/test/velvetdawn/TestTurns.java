package test.velvetdawn;

import static org.junit.Assert.*;
import org.junit.Test;
import test.BaseTest;
import velvetdawn.VelvetDawn;
import velvetdawn.constants.AttributeKeys;
import velvetdawn.models.Coordinate;
import velvetdawn.models.Phase;
import velvetdawn.models.config.Config;

import java.util.ArrayList;

public class TestTurns extends BaseTest {

    /** Test if the turn should end */
    @Test
    public void test_check_end_turn_case_in_setup_from_time() throws Exception {
        var config = this.getConfig();
        config.setupTime = 1;
        var velvetDawn = new VelvetDawn(config);

        velvetDawn.players.join("player1", "password");
        velvetDawn.players.join("player2", "password");
        velvetDawn.game.startSetupPhase();

        assertEquals(velvetDawn.game.phase, Phase.Setup);
        Thread.sleep(2000);
        velvetDawn.game.turns.checkEndTurnCase();

        assertEquals(velvetDawn.game.phase, Phase.Game);
    }

    /** Test if the turn should end */
    @Test
    public void test_check_end_turn_case_in_setup_when_ready() throws Exception {
        var velvetDawn = new VelvetDawn(this.getConfig());

        var p1 = velvetDawn.players.join("player1", "password");
        var p2 = velvetDawn.players.join("player2", "password");
        velvetDawn.game.startSetupPhase();

        p1.ready = true;
        p2.ready = true;
        velvetDawn.game.turns.checkEndTurnCase();

        assertEquals(velvetDawn.game.phase, Phase.Game);
    }

    /** Test if the turn should end */
    @Test
    public void test_check_end_turn_case_in_game_from_time() throws Exception {
        var config = this.getConfig();
        config.turnTime = 1000;
        var velvetDawn = new VelvetDawn(config);

        var p1 = velvetDawn.players.join("player1", "password");
        var p2 = velvetDawn.players.join("player2", "password");
        velvetDawn.game.startGamePhase();
        velvetDawn.game.turns.updateTurnStartTime();
        assertEquals(p1.team, velvetDawn.game.turns.getActiveTurn());

        Thread.sleep(2000);
        velvetDawn.game.turns.checkEndTurnCase();
        assertEquals(p2.team, velvetDawn.game.turns.getActiveTurn());
    }

    /** Test if the turn should end */
    @Test
    public void test_check_end_turn_case_in_game_when_ready() throws Exception {
        var config = this.getConfig();
        var velvetDawn = new VelvetDawn(config);

        var p1 = velvetDawn.players.join("player1", "password");
        var p2 = velvetDawn.players.join("player2", "password");
        velvetDawn.game.startGamePhase();

        assertEquals(p1.team, velvetDawn.game.turns.getActiveTurn());

        p1.ready = true;
        velvetDawn.game.turns.checkEndTurnCase();
        assertEquals(p2.team, velvetDawn.game.turns.getActiveTurn());
    }

    /** Test that when a turn begins the entity movement is set to it's range */
    @Test
    public void test_begin_next_turn_resets_entity_movement() throws Exception {
        Config config = this.getConfig();
        VelvetDawn velvetDawn = new VelvetDawn(config);

        // Setup the game state
        var p1 = velvetDawn.players.join("player1", "null");
        velvetDawn.game.phase = Phase.Lobby;
        velvetDawn.game.setup.updateSetup("testing:commander", 1);
        velvetDawn.game.startSetupPhase();
        velvetDawn.game.setup.placeEntity(p1, "testing:commander", new Coordinate((float) (this.getConfig().map.width / 2), 0));

        var unit = new ArrayList<>(p1.entities).get(0);
        assertEquals(0, unit.attributes.get("movement.remaining").toNumber(), 0);

        velvetDawn.game.startGamePhase();

        assertEquals(
            unit.attributes.get(AttributeKeys.EntityRemainingMoves),
            unit.attributes.get("movement.range")
        );
    }

    /** This will test getting the active turn and beginning a new turn */
    @Test
    public void test_begin_next_turn_and_get_active_turn() throws Exception {
        var velvetDawn = new VelvetDawn(this.getConfig());

        var p1 = velvetDawn.players.join("player1", "password");
        var p2 = velvetDawn.players.join("player2", "password");
        assertNull(velvetDawn.game.turns.getActiveTurn());

        velvetDawn.game.startGamePhase();

        assertEquals(p1.team, velvetDawn.game.turns.getActiveTurn());

        velvetDawn.game.turns.ready(p1);

        velvetDawn.game.turns.beginNextTurn();

        assertFalse(p1.ready);
        assertFalse(p2.ready);

        assertEquals(p2.team, velvetDawn.game.turns.getActiveTurn());

        velvetDawn.game.turns.beginNextTurn();

        assertEquals(p1.team, velvetDawn.game.turns.getActiveTurn());
    }

    @Test
    public void test_check_all_players_ready_during_setup() throws Exception {
        Config config = this.getConfig();
        var velvetDawn = new VelvetDawn(config);

        velvetDawn.game.setup.updateSetup("testing:commander", 1);
        var p1 = velvetDawn.players.join("player1", "password");
        var p2 = velvetDawn.players.join("player2", "password");
        var p3 = velvetDawn.players.join("player3", "password");

        velvetDawn.game.startSetupPhase();
        velvetDawn.map.generate();

        velvetDawn.game.setup.placeEntity(p1, "testing:commander", new Coordinate(5, 0));
        velvetDawn.game.setup.placeEntity(p2, "testing:commander", new Coordinate(10, 6));
        velvetDawn.game.setup.placeEntity(p3, "testing:commander", new Coordinate(2, 10));

        velvetDawn.game.turns.ready(p1);
        assertFalse(velvetDawn.game.turns.checkAllPlayersReady());
        velvetDawn.game.turns.ready(p2);
        assertFalse(velvetDawn.game.turns.checkAllPlayersReady());
        velvetDawn.game.turns.ready(p3);
        assertTrue(velvetDawn.game.turns.checkAllPlayersReady());

        velvetDawn.game.startGamePhase();

        velvetDawn.game.turns.ready(p2);
        assertFalse(velvetDawn.game.turns.checkAllPlayersReady());
        velvetDawn.game.turns.ready(p3);
        assertFalse(velvetDawn.game.turns.checkAllPlayersReady());
        velvetDawn.game.turns.ready(p1);
        assertTrue(velvetDawn.game.turns.checkAllPlayersReady());
    }

    @Test
    public void test_ready_setup_placed_commander() throws Exception {
        var velvetDawn = new VelvetDawn(this.getConfig());

        var p1 = velvetDawn.players.getPlayer("player1");
        velvetDawn.game.phase = Phase.Setup;

        // No commanders played so can't ready up
        assertThrows(Exception.class, () ->
            velvetDawn.game.turns.ready(p1));
    }

    @Test
    public void test_ready_unready() throws Exception {
        var velvetDawn = this.prepareGame();
        var p1 = velvetDawn.players.getPlayer("player1");
        var p2 = velvetDawn.players.getPlayer("player2");

        velvetDawn.game.turns.ready(p1);
        assertTrue(p1.ready);
        assertFalse(p2.ready);

        velvetDawn.game.turns.ready(p2);
        assertTrue(p1.ready);
        assertTrue(p2.ready);

        velvetDawn.game.turns.unready(p1);
        assertFalse(p1.ready);
        assertTrue(p2.ready);

        velvetDawn.game.turns.unready(p2);
        assertFalse(p1.ready);
        assertFalse(p2.ready);
    }

    @Test
    public void test_update_turn_start_time() throws Exception {
        var velvetDawn = this.prepareGame();
        var currentTurnStart = velvetDawn.game.turns.currentTurnData().getTurnStart();

        Thread.sleep(10);

        var updatedTime = velvetDawn.game.turns.updateTurnStartTime();
        assertEquals(
                Math.round(updatedTime),
                Math.round(velvetDawn.game.turns.currentTurnData().getTurnStart()));

        assertNotEquals(
                currentTurnStart.longValue(),
                velvetDawn.game.turns.currentTurnData().getTurnStart().longValue());
    }

    @Test
    public void test_current_turn_time() throws Exception {
        var config = this.getConfig();
        var velvetDawn = new VelvetDawn(config);

        config.turnTime = 10;
        assertEquals(10, velvetDawn.game.turns.currentTurnTime());

        config.turnTime = 500;
        assertEquals(500, velvetDawn.game.turns.currentTurnTime());

        // Test setup is always 5 mins
        config.setupTime = 5;
        velvetDawn.game.phase = Phase.Setup;
        assertEquals(5, velvetDawn.game.turns.currentTurnTime());
    }
}
