package test.velvetdawn.datapacks;

import static org.junit.Assert.*;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.VelvetDawn;
import velvetdawn.models.instances.attributes.Attribute;
import velvetdawn.utils.Json;


public class TestAttributes extends BaseTest {

    @Test
    public void test_attributes_parsing() throws Exception {
        var config = this.getConfig();

        // Missing id
        assertThrows(Exception.class, () -> {
            Attribute.load(new VelvetDawn(config), "", new Json());
        });

        // Malformed id
        assertThrows(Exception.class, () -> {
            Attribute.load(new VelvetDawn(config), "", new Json().set("id", "%id"));
        });

        // Malformed name
        assertThrows(Exception.class, () -> {
            Attribute.load(new VelvetDawn(config), "", new Json()
                    .set("id", "example")
                    .set("name", "$£@"));
        });

        // Invalid icon
        assertThrows(Exception.class, () -> {
            Attribute.load(new VelvetDawn(config), "", new Json()
                    .set("id", "example")
                    .set("name", "Fine Name")
                    .set("icon", false));
        });

        // Invalid key
        assertThrows(Exception.class, () -> {
            Attribute.load(new VelvetDawn(config), "", new Json()
                    .set("id", "example")
                    .set("name", "Fine Name")
                    .set("invalid-key", false));
        });

        Attribute.load(new VelvetDawn(config), "", new Json()
                .set("id", "example")
                .set("name", "Fine Name")
                .set("icon", "An icon")
                .set("default", 100));
    }
}
