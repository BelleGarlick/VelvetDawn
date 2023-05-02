package test.velvetdawn.datapacks.entities;

import org.junit.Test;
import velvetdawn.core.mechanics.abilities.Abilities;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;

import static org.junit.Assert.assertThrows;


public class TestUnitAbilityParsing extends test.BaseTest {

    @Test
    public void test_abilities_parsing() throws Exception {
        var velvetDawn = this.prepareGame();

        // Test no name
        assertThrows(Exception.class, () ->
                        new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson())));
        new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson().set("name", "hi")));

        // Enabled is not a list
        assertThrows(Exception.class, () ->
                new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson()
                .set("enabled", false)
                .set("name", "hi"))));

        // Hidden is not a list
        assertThrows(Exception.class, () ->
                new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson()
                            .set("hidden", false)
                            .set("name", "hi"))));

        // actions is not a list
        assertThrows(Exception.class, () ->
                new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson()
                        .set("actions", false)
                        .set("name", "hi"))));

        // Require is not a list of strings
        assertThrows(Exception.class, () ->
                new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson()
                        .set("requires", false)
                        .set("name", "hi"))));
        assertThrows(Exception.class, () ->
                new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson()
                        .set("requires", AnyList.of(new AnyJson()))
                        .set("name", "hi"))));
        // Random key
        assertThrows(Exception.class, () ->
        new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson()
                        .set("random-key", "false")
                        .set("name", "hi"))));

        // Valid
        new Abilities().load(velvetDawn, "", AnyList.of(new AnyJson()
                .set("enabled", AnyList.of(new AnyJson().set("if", "self").set("eq", "example")))
                        .set("enabled", AnyList.of(new AnyJson().set("if", "self").set("ne", "example")))
                        .set("actions", AnyList.of(new AnyJson().set("modify", "self.health").set("add", 1)))
                        .set("name", "hi")));
    }
}