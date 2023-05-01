package test.velvetdawn.entities;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.mechanics.upgrades.Upgrade;
import velvetdawn.core.models.Coordinate;

import java.util.ArrayList;
import java.util.List;

import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThrows;


public class TestEntityUpgrades extends BaseTest {

    private String getUpgradeIdByName(List<Upgrade> upgrades, String name) {
        for (Upgrade upgrade: upgrades) {
            if (upgrade.name.equals(name))
                return upgrade.id;
        }
        return null;
    }

    /** The testing:upgrades unit has predefined upgrades specifically
    for this test to make sure that hidden/enabled and requirements all
    work correctly.*/
    @Test
    public void test_upgrading() throws Exception {
        var velvetDawn = this.prepareGame();
        
        var upgradable_unit = velvetDawn.entities.getAtPosition(new Coordinate(4, 0)).get(0);
        var upgrades = new ArrayList<>(velvetDawn.datapacks.entities.get(upgradable_unit.datapackId).upgrades.upgrades.values());

        // Invalid upgrade
        assertThrows(Exception.class, () ->
            upgradable_unit.upgrades.upgrade("random key"));

        // Upgrade already owned
        upgradable_unit.upgrades.upgrade("health_1");
        assertThrows(Exception.class, () ->
                upgradable_unit.upgrades.upgrade("health_1"));

        // Missing upgrade requirement;
        assertThrows(Exception.class, () ->
                upgradable_unit.upgrades.upgrade(upgrades.get(upgrades.size() - 1).id));

        // Test hidden elements can't run as missing tag
        assertThrows(Exception.class, () ->
                upgradable_unit.upgrades.upgrade("health_2"));
        upgradable_unit.tags.add("visible");
        upgradable_unit.upgrades.upgrade("health_2");

        // Test disable elements can't run as missing tag
        assertThrows(Exception.class, () ->
                upgradable_unit.upgrades.upgrade(getUpgradeIdByName(upgrades, "Movement")));
        upgradable_unit.tags.add("enabled");
        upgradable_unit.upgrades.upgrade(getUpgradeIdByName(upgrades, "Movement"));

        upgradable_unit.upgrades.upgrade(getUpgradeIdByName(upgrades, "Super"));

        assertTrue(upgradable_unit.tags.contains("upgrade-added"));
    }   

    @Test
    public void test_fetching_upgrades() throws Exception {
        var velvetDawn = this.prepareGame();

        var upgradable_unit = velvetDawn.entities.getAtPosition(new Coordinate(4, 0)).get(0);

        var upgrades = upgradable_unit.upgrades.getUpgradeUpdates();
        assertEquals(0, upgrades.upgraded.size());
        assertEquals(1, upgrades.upgrades.size());
        assertEquals(1, upgrades.missingRequirements.size());
        assertEquals(1, upgrades.hidden.size());
        assertEquals(1, upgrades.disabled.size());

        upgradable_unit.upgrades.upgrade("health_1");
        upgradable_unit.tags.add("visible");
        upgrades = upgradable_unit.upgrades.getUpgradeUpdates();
        assertEquals(1, upgrades.upgraded.size());
        assertEquals(1, upgrades.upgrades.size());
        assertEquals(1, upgrades.missingRequirements.size());
        assertEquals(0, upgrades.hidden.size());
        assertEquals(1, upgrades.disabled.size());

        upgradable_unit.upgrades.upgrade("health_2");
        upgradable_unit.tags.add("enabled");
        upgrades = upgradable_unit.upgrades.getUpgradeUpdates();
        assertEquals(2, upgrades.upgraded.size());
        assertEquals(1, upgrades.upgrades.size());
        assertEquals(1, upgrades.missingRequirements.size());
        assertEquals(0, upgrades.hidden.size());
        assertEquals(0, upgrades.disabled.size());

        upgradable_unit.upgrades.upgrade("movement");
        upgrades = upgradable_unit.upgrades.getUpgradeUpdates();
        assertEquals(3, upgrades.upgraded.size());
        assertEquals(1, upgrades.upgrades.size());
        assertEquals(0, upgrades.missingRequirements.size());
        assertEquals(0, upgrades.hidden.size());
        assertEquals(0, upgrades.disabled.size());

        upgradable_unit.upgrades.upgrade("testing:upgradable-upgrade-3");
        upgrades = upgradable_unit.upgrades.getUpgradeUpdates();
        assertEquals(4, upgrades.upgraded.size());
        assertEquals(0, upgrades.upgrades.size());
        assertEquals(0, upgrades.missingRequirements.size());
        assertEquals(0, upgrades.hidden.size());
        assertEquals(0, upgrades.disabled.size());
    }
}