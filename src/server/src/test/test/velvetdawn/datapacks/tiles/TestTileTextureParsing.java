package test.velvetdawn.datapacks.tiles;

import org.junit.Test;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;
import velvetdawn.core.models.anytype.AnyNull;
import velvetdawn.core.models.datapacks.tiles.TileTextures;

import java.util.List;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertThrows;


public class TestTileTextureParsing extends test.BaseTest {

    @Test
    public void test_tile_textures_parsing_color() throws Exception {
        // Bad key
        assertThrows(Exception.class, () -> new TileTextures().load("", new AnyJson().set("colour", 0).set("color", "#000000")));

        // Type is wrong
        assertThrows(Exception.class, () -> new TileTextures().load("", new AnyJson().set("color", 0)));

        // String color
        var textures = new TileTextures().load("", new AnyJson().set("color", "example"));
        assertTrue(textures.colors.contains("example"));
        assertEquals(1, textures.colors.size());

        // List color
        textures = new TileTextures().load("", new AnyJson().set("color", AnyList.of("example", "example2")));
        assertTrue(textures.colors.contains("example"));
        assertTrue(textures.colors.contains("example2"));

        // AnyJson color
        textures = new TileTextures().load("", new AnyJson()
                .set("color", new AnyJson()
                        .set("example", 2)
                        .set("example2", 1)));
        assertTrue(textures.colors.contains("example"));
        assertTrue(textures.colors.contains("example2"));
        assertEquals(3, textures.colors.size());

        assertTrue(List.of("example", "example2").contains(textures.chooseColor().toString()));
        assertTrue(textures.chooseImage() instanceof AnyNull);
    }

    @Test
    public void test_tile_textures_parsing_image() throws Exception {
        // Image is wrong
        assertThrows(Exception.class, () -> new TileTextures().load("", new AnyJson()
                .set("color", "example")
                .set("image", 0)));

        // String image
        var textures = new TileTextures().load("", new AnyJson()
                .set("color", "example")
                .set("image", "example"));
        assertTrue(textures.images.contains("example"));
        assertEquals(1, textures.images.size());

        // List image
        textures = new TileTextures().load("", new AnyJson()
                .set("color", "example")
                .set("image", AnyList.of("example", "example2")));
        assertTrue(textures.images.contains("example"));
        assertTrue(textures.images.contains("example2"));

        // AnyJson image
        textures = new TileTextures().load("", new AnyJson()
                .set("color", "example")
                .set("image", new AnyJson()
                        .set("example", 2)
                        .set("example2", 1)));
        assertTrue(textures.images.contains("example"));
        assertTrue(textures.images.contains("example2"));
        assertEquals(3, textures.images.size());

        assertTrue(List.of("example", "example2").contains(textures.chooseColor().toString()));
        assertTrue(List.of("example", "example2").contains(textures.chooseImage().toString()));
    }
}