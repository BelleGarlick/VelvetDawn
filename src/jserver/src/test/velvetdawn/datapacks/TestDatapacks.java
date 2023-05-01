package test.velvetdawn.datapacks;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.core.VelvetDawn;
import velvetdawn.core.datapacks.DatapackManager;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.utils.Path;

import java.util.stream.Collectors;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertFalse;
import static junit.framework.TestCase.assertNull;
import static junit.framework.TestCase.assertTrue;


// TODO Test overriding entity from files
// TODO Test loading entity from json works as expected
// TODO Test loading resources with overriding


public class TestDatapacks extends BaseTest {

    /** Test entity id is correct */
    @Test
    public void test_construct_id() throws Exception {
        var velvetDawn = new VelvetDawn(new Config());
        var datapackPath = new Path("example").getChild("entity");

        ConstructIdInterface _id = (Path path, boolean fileType, AnyJson data) -> {
            try {
                return velvetDawn.datapacks.constructId("example", datapackPath, path, fileType, data);
            } catch (Exception e) {
                return null;
            }
        };

        assertEquals("example:entity1", _id.run(datapackPath.getChild("entity1.json"), false, null));
        assertEquals("example:entity1.json", _id.run(datapackPath.getChild("entity1.json"), true, null));
        assertEquals("example:_entity1", _id.run(datapackPath.getChild("_entity1.json"), false, null));
        assertEquals(
            "example:deep.deeper.deepest._entity1",
            _id.run(datapackPath
                    .getChild("deep")
                    .getChild("deeper")
                    .getChild("deepest")
                    .getChild("_entity1.json"), false, null)
        );
        assertEquals("other:ahh", _id.run(datapackPath.getChild("entity1.json"), false, new AnyJson().set("id", "other:ahh")));
    }

    /** Test that files are loaded correctly into concrete and abstracts dirs */
    @Test
    public void test_load_items_in_dir() throws Exception {
        var config = new Config();
        var velvetDawn = new VelvetDawn(config);

        var test_path = new Path("pack");
        var entities_path = test_path.getChild("entity");

        if (test_path.exists())
            test_path.rmtree();

        test_path.mkdir();
        entities_path.mkdir();

        entities_path.getChild("example-a.json").writeJson(new AnyJson()
                .set("abstract", true)
                .set("name", "eaxmple_a"));

        entities_path.getChild("example-b.json").writeJson(new AnyJson()
                .set("name", "example_b"));

        var files = velvetDawn.datapacks.loadItemsInDir(test_path.getChild("entity"), "pack");
        var keys = files.keySet()
                .stream()
                .map(x -> x.toPath().toAbsolutePath().toString())
                .collect(Collectors.toSet());
        assertFalse(keys.contains(entities_path.getChild("pack:example-a.json").absolutePath()));
        assertTrue(keys.contains(entities_path.getChild("example-b.json").absolutePath()));
        assertTrue(velvetDawn.datapacks.abstractDefinitions.containsKey("pack:example-a"));

        test_path.rmtree();
    }

    @Test
    public void test_extend() throws Exception {
        var velvetDawn = new VelvetDawn(this.getConfig());
        velvetDawn.datapacks.abstractDefinitions.put("a", new AnyJson()
                .set("b", "c"));
        velvetDawn.datapacks.abstractDefinitions.put("d", new AnyJson()
                .set("e", AnyList.of(Any.from("f"), Any.from("g")))
                .set("h", 1));

        // Check no extension
        var extended = velvetDawn.datapacks.extend(new AnyJson());
        assertEquals(0, extended.keys().size());

        // Check no extension even with the extension tag
        extended = velvetDawn.datapacks.extend(new AnyJson().set("exends", new AnyList()));
        assertEquals(1, extended.keys().size());

        // Check extending from 'a' but not 'd'
        extended = velvetDawn.datapacks.extend(new AnyJson().set("extends", AnyList.of("a")));
        assertEquals(2, extended.keys().size());
        assertEquals("c", extended.get("b").toString());
        assertNull(extended.get("d"));

        // Check extending from d but not a
        extended = velvetDawn.datapacks.extend(new AnyJson().set("extends", AnyList.of("d")));
        assertEquals(3, extended.keys().size());
        assertEquals(1.0, extended.get("h").toNumber(), 0.001);
        assertNull(extended.get("b"));

        // Test extends from both
        extended = velvetDawn.datapacks.extend(new AnyJson().set("extends", AnyList.of("a", "d")));
        assertEquals(4, extended.keys().size());
        assertEquals(1.0, extended.get("h").toNumber(), 0.001);
        assertEquals("c", extended.get("b").toString());
    }

    /** Test copying dicts merged works */
    @Test
    public void test_copy_dict() throws Exception {
        var base = new AnyJson()
                .set("a", "string")
                .set("b", 0)
                .set("c", true)
                .set("e", new AnyJson()
                        .set("f", "g"))
                .set("h", AnyList.of("i"));

        var merged = new AnyJson();
        DatapackManager.mergeJson(merged, base);

        assertEquals(merged.get("a").toString(), "string");

        // Test updating again works in merged but doesn't affect base
        DatapackManager.mergeJson(merged, new AnyJson()
                .set("a", "not string")
                .set("e", new AnyJson().set("z", "y"))
                .set("h", AnyList.of("j")));

        // Updating doesn't update original
        assertEquals(merged.get("a").toString(), "not string");
        assertEquals(base.get("a").toString(), "string");

        assertEquals("g", ((AnyJson) merged.get("e")).get("f").toString());
        assertEquals("y", ((AnyJson) merged.get("e")).get("z").toString());
        assertNull(((AnyJson) base.get("e")).get("z"));

        assertEquals(2, ((AnyList) merged.get("h")).size());
        assertEquals(1, ((AnyList) base.get("h")).size());
    }

    private interface ConstructIdInterface {
        String run(Path path, boolean fileType, AnyJson data);
    }
}
