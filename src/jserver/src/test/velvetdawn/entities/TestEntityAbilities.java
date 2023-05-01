package test.velvetdawn.entities;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.models.Coordinate;

import java.util.ArrayList;

import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThrows;


public class TestEntityAbilities extends BaseTest {

    /** The testing:abilitied unit has predefined abilities specifically
    for this test to make sure that hidden/enabled all work correctly.
    */
    @Test
    public void test_abilities() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(6, 0)).get(0);
        var abilities = new ArrayList<>(velvetDawn.datapacks.entities.get(unit.datapackId).abilities.abilities.values());

        // Invalid ability
        assertThrows(Exception.class, () ->
            unit.abilities.perform("random key"));

        unit.abilities.perform(abilities.get(0).id);
        assertTrue(unit.tags.contains("ability1-ran"));

        // Test hidden elements can't run as missing tag
        var ability2Id = abilities.stream()
                .filter(x -> x.name.equals("Ability 2"))
                .findFirst()
                .get()
                .id;
        assertThrows(Exception.class, () ->
            unit.abilities.perform(ability2Id));
        unit.tags.add("visible");
        unit.abilities.perform(ability2Id);
        assertTrue(unit.tags.contains("ability2-ran"));

        // Test disable elements can't run as missing tag
        var ability3Id = abilities.stream()
                .filter(x -> x.name.equals("Ability 3"))
                .findFirst()
                .get()
                .id;
        assertThrows(Exception.class, () ->
            unit.abilities.perform(ability3Id));
        unit.tags.add("enabled");
        unit.abilities.perform(ability3Id);
        assertTrue(unit.tags.contains("ability3-ran"));
    }
                    
    @Test
    public void test_fetching_abilities() throws Exception {
        var velvetDawn = this.prepareGame();

        var unit = velvetDawn.entities.getAtPosition(new Coordinate(6, 0)).get(0);
        var abilitiesList = new ArrayList<>(velvetDawn.datapacks.entities.get(unit.datapackId).abilities.abilities.values());

        var abilities = unit.abilities.getAbilityUpdates();
        assertEquals(1, abilities.abilities.size());
        assertEquals(1, abilities.hidden.size());
        assertEquals(1, abilities.disabled.size());

        unit.tags.add("visible");
        unit.abilities.perform(abilitiesList.stream()
                .filter(x -> x.name.equals("Ability 2"))
                .findFirst()
                .get()
                .id);
        abilities = unit.abilities.getAbilityUpdates();
        assertEquals(2, abilities.abilities.size());
        assertEquals(0, abilities.hidden.size());
        assertEquals(1, abilities.disabled.size());

        unit.tags.add("enabled");
        unit.abilities.perform(abilitiesList.stream()
                .filter(x -> x.name.equals("Ability 3"))
                .findFirst()
                .get()
                .id);
        abilities = unit.abilities.getAbilityUpdates();
        assertEquals(3, abilities.abilities.size());
        assertEquals(0, abilities.hidden.size());
        assertEquals(0, abilities.disabled.size());
    }
}


