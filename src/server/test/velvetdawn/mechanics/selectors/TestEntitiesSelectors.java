package velvetdawn.mechanics.selectors;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.mechanics.selectors.SelectorEnemies;
import velvetdawn.core.mechanics.selectors.SelectorEntities;
import velvetdawn.core.mechanics.selectors.SelectorFriendlies;
import velvetdawn.core.mechanics.selectors.Selectors;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.instances.WorldInstance;

import java.util.ArrayList;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;


public class TestEntitiesSelectors extends BaseTest {

    /* Test the unit selectors get the correct selection
    for the different instance types.
    */

    @Test
    public void test_selector_units() throws Exception {
        var velvetDawn = this.prepareGame();

        var units_selector = Selectors.get(velvetDawn, "0", "entities");
        var friendlies_selector = Selectors.get(velvetDawn, "0", "friendlies");
        var selector_enemies = Selectors.get(velvetDawn, "0", "enemies");

        assertTrue(units_selector instanceof SelectorEntities);
        assertTrue(friendlies_selector instanceof SelectorFriendlies);
        assertTrue(selector_enemies instanceof SelectorEnemies);
    }

    @Test
    public void test_selectors_from_unit() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = new ArrayList<>(velvetDawn.entities.getAtPosition(new Coordinate(5, 0))).get(0);

        var unitsSelector = Selectors.get(velvetDawn, unit.datapackId, "entities");
        var friendliesSelector = Selectors.get(velvetDawn, unit.datapackId, "friendlies");
        var selectorEnemies = Selectors.get(velvetDawn, unit.datapackId, "enemies");

        var all_units = unitsSelector.getChainedSelection(unit);
        var friendlies = friendliesSelector.getChainedSelection(unit);
        var enemies = selectorEnemies.getChainedSelection(unit);

        assertEquals(4, all_units.size());
        assertEquals(3, friendlies.size());
        assertEquals(1, enemies.size());
    }

    @Test
    public void test_selectors_from_tile_and_world() throws Exception {
        var velvetDawn = this.prepareGame();

        var tile = velvetDawn.map.getTile(new Coordinate(5, 0));

        // Get selectors
        var units_selector = Selectors.get(velvetDawn, tile.datapackId, "entities");
        var friendliesSelector = Selectors.get(velvetDawn, tile.datapackId, "friendlies");
        var enemiesSelector = Selectors.get(velvetDawn, tile.datapackId, "enemies");

        // From tile perspective
        var all_units = units_selector.getChainedSelection(tile);
        var friendlies = friendliesSelector.getChainedSelection(tile);
        var enemies = enemiesSelector.getChainedSelection(tile);
        assertEquals(4, all_units.size());
        assertEquals(3, friendlies.size());
        assertEquals(1, enemies.size());

        // From world perspective
        all_units = units_selector.getChainedSelection(WorldInstance.getInstance());
        friendlies = friendliesSelector.getChainedSelection(WorldInstance.getInstance());
        enemies = enemiesSelector.getChainedSelection(WorldInstance.getInstance());
        assertEquals(4, all_units.size());
        assertEquals(3, friendlies.size());
        assertEquals(1, enemies.size());

        // Switch turns
        velvetDawn.game.turns.beginNextTurn();

        // From tile perspective
        friendlies = friendliesSelector.getChainedSelection(tile);
        enemies = enemiesSelector.getChainedSelection(tile);
        assertEquals(1, friendlies.size());
        assertEquals(3, enemies.size());

        // From world perspective
        friendlies = friendliesSelector.getChainedSelection(WorldInstance.getInstance());
        enemies = enemiesSelector.getChainedSelection(WorldInstance.getInstance());
        assertEquals(1, friendlies.size());
        assertEquals(3, enemies.size());
    }
}
