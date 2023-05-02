package velvetdawn.datapacks.tiles;

import org.junit.Test;
import velvetdawn.BaseTest;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.datapacks.tiles.TileDefinition;
import velvetdawn.core.models.instances.attributes.AttributesDefinition;

import static junit.framework.TestCase.assertEquals;
import static org.junit.Assert.assertThrows;


public class TestTileParsing extends BaseTest {

    @Test
    public void test_tile_movement() throws Exception {
        var velvetDawn = this.prepareGame();

        // Type is wrong
        assertThrows(Exception.class, () ->
                new TileDefinition("", "").parseMovement(
                        "", new AttributesDefinition(), new AnyJson().set("weight", "dsa")));

        // Must be at least 0
        assertThrows(Exception.class, () ->
                new TileDefinition("", "").parseMovement(
                        "", new AttributesDefinition(), new AnyJson().set("weight", -1)));

        // Wrong type
        assertThrows(Exception.class, () ->
                new TileDefinition("", "").parseMovement(
                        "", new AttributesDefinition(), new AnyJson().set("traversable", "kjl")));

        // Wrong key
        assertThrows(Exception.class, () ->
                new TileDefinition("", "").parseMovement(
                        "", new AttributesDefinition(), new AnyJson().set("traversable", true).set("random-key", false)));

        // Valid
        var attributes = new AttributesDefinition();
        new TileDefinition("", "").parseMovement("", attributes, new AnyJson()
                .set("traversable", false)
                .set("weight", 5)
                .set("notes", "Example"));

        assertEquals(false, attributes.get("movement.traversable").value.toBool());
        assertEquals(5, attributes.get("movement.weight").value.toNumber(), 0);
    }
}
