package test.velvetdawn.mechanics.selectors;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.mechanics.selectors.SelectorEntities;
import velvetdawn.mechanics.selectors.SelectorSelf;
import velvetdawn.mechanics.selectors.Selectors;
import velvetdawn.mechanics.selectors.WorldSelector;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyNull;
import velvetdawn.models.instances.WorldInstance;

import java.util.ArrayList;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;


public class TestWorldSelector extends BaseTest {

    /** Test world selector return the world instance */
    @Test
    public void test_selector_parsing() throws Exception {
        var vd = this.prepareGame();

        var selector = Selectors.get(vd, "0", "world.health.max");
        assertTrue(selector instanceof WorldSelector);

        var selection = selector.getChainedSelection(null);
        assertTrue(new ArrayList<>(selection).get(0) instanceof WorldInstance);
    }
}
