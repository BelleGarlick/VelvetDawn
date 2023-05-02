package test.velvetdawn.datapacks;

import static org.junit.Assert.*;

import org.junit.Test;
import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.instances.attributes.AttributeDefinition;

public class TestAttributes extends test.BaseTest {

    @Test
    public void test_attributes_parsing() throws Exception {
        var config = this.getConfig();

        // Missing id
        assertThrows(Exception.class, () -> {
            AttributeDefinition.load(new VelvetDawn(config), "", new AnyJson());
        });

        // Malformed id
        assertThrows(Exception.class, () -> {
            AttributeDefinition.load(new VelvetDawn(config), "", new AnyJson().set("id", "%id"));
        });

        // Malformed name
        assertThrows(Exception.class, () -> {
            AttributeDefinition.load(new VelvetDawn(config), "", new AnyJson()
                    .set("id", "example")
                    .set("name", "$£@"));
        });

        // Invalid icon
        assertThrows(Exception.class, () -> {
            AttributeDefinition.load(new VelvetDawn(config), "", new AnyJson()
                    .set("id", "example")
                    .set("name", "Fine Name")
                    .set("icon", false));
        });

        // Invalid key
        assertThrows(Exception.class, () -> {
            AttributeDefinition.load(new VelvetDawn(config), "", new AnyJson()
                    .set("id", "example")
                    .set("name", "Fine Name")
                    .set("invalid-key", false));
        });

        AttributeDefinition.load(new VelvetDawn(config), "", new AnyJson()
                .set("id", "example")
                .set("name", "Fine Name")
                .set("icon", "An icon")
                .set("default", 100));
    }
}
