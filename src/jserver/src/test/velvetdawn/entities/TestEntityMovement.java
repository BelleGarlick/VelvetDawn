package test.velvetdawn.entities;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.constants.AttributeKeys;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.Phase;
import velvetdawn.core.models.anytype.Any;

import java.util.ArrayList;
import java.util.List;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertFalse;
import static org.junit.Assert.assertThrows;


public class TestEntityMovement extends BaseTest {

    /* Test the entities movement is validated correctly on the server */

    @Test
    public void test_move() throws Exception {
        var velvetDawn = this.prepareGame();

        var entity = velvetDawn.entities.list().get(0);
        var player2entity = velvetDawn.entities.list().get(1);

        var firstPos = entity.position;

        velvetDawn.game.phase = Phase.Lobby;
        assertThrows(Exception.class, () ->
            velvetDawn.entities.movement.move(entity, List.of(
                    firstPos, firstPos.down())));
        velvetDawn.game.phase = Phase.Game;
        
        velvetDawn.game.turns.beginNextTurn();
        assertThrows(Exception.class, () ->
                velvetDawn.entities.movement.move(entity, List.of(
                        firstPos, firstPos.down())));
        velvetDawn.game.turns.beginNextTurn();

        assertThrows(Exception.class, () ->
            velvetDawn.entities.movement.move(entity, List.of(
                    firstPos.up(), firstPos.up().up())));

        assertThrows(Exception.class, () -> 
            velvetDawn.entities.movement.move(player2entity, List.of(
                    firstPos.up(),
                    firstPos.up().up())));

        assertEquals(2, entity.attributes.get(AttributeKeys.EntityRemainingMoves).toNumber(), 0);

        velvetDawn.entities.movement.move(entity, List.of(
                firstPos, firstPos.down()));

        assertEquals(1, entity.attributes.get(AttributeKeys.EntityRemainingMoves).toNumber(), 0);

        assertEquals(entity.position, firstPos.down());
    }

    @Test
    public void test_validate_entity_traversing_path() throws Exception {
        var velvetDawn = this.prepareGame();
        var entity = velvetDawn.entities.list().get(0);

        // Test invalid start tile
        assertThrows(Exception.class, () -> 
            velvetDawn.entities.movement.validateEntityTraversingPath(entity, List.of(new Coordinate())));

        // Test empty tile in sequence
        var firstPos = entity.position;
        assertThrows(Exception.class, () ->
                velvetDawn.entities.movement.validateEntityTraversingPath(entity, List.of(new Coordinate(), new Coordinate().left())));

        // Test tiles not neighbours
        assertThrows(Exception.class, () ->
                velvetDawn.entities.movement.validateEntityTraversingPath(entity, List.of(firstPos, new Coordinate())));

        // Test unknown tile error
        var tile = velvetDawn.map.getTile(firstPos.left());
        tile.datapackId = "unknown_tile";
        assertThrows(Exception.class, () ->
            velvetDawn.entities.movement.validateEntityTraversingPath(entity, List.of(firstPos,
                firstPos.left())));

        // Test tile not traversable
        tile = velvetDawn.map.getTile(new Coordinate(firstPos.x + 1, firstPos.y));
        tile.attributes.set(AttributeKeys.TileTraversable, Any.from(false));
        assertFalse(tile.attributes.get(AttributeKeys.TileTraversable).toBool());
        assertThrows(Exception.class, () ->
            velvetDawn.entities.movement.validateEntityTraversingPath(entity, List.of(
                firstPos, firstPos.right()
            )));

        // Too long
        List<Coordinate> items = new ArrayList<>();
        for (int i = 0; i < 10; i++)
            items.add(new Coordinate(firstPos.x, firstPos.y + i));
        assertThrows(Exception.class, () ->
            velvetDawn.entities.movement.validateEntityTraversingPath(entity, items));

        // Just right
        assertEquals(2.0, entity.attributes.get("movement.remaining").toNumber(), 0.001);
        var remainingMoves = velvetDawn.entities.movement.validateEntityTraversingPath(entity, List.of(
                firstPos,
                firstPos.down(),
                firstPos.down().down()
        ));
        assertEquals(0, remainingMoves);
    }
}