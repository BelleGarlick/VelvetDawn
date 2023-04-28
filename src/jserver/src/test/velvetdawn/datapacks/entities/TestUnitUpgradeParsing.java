package test.velvetdawn.datapacks.entities;

import org.junit.Test;
import test.BaseTest;
import velvetdawn.mechanics.upgrades.Upgrades;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.anytype.AnyList;

import java.util.List;

import static org.junit.Assert.assertThrows;


public class TestUnitUpgradeParsing extends BaseTest {

    @Test
    public void test_upgrade_parsing() throws Exception {
        var velvetDawn = this.prepareGame();

        // Test no name
        assertThrows(Exception.class, () ->
                new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson())));
        new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson().set("name", "hi")));

        // Type id is wrong type
        assertThrows(Exception.class, () ->
            new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson()
                    .set("id", false)
                    .set("name", "hi"))));

        // Enabled is not a list
        assertThrows(Exception.class, () ->
            new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson()
                    .set("enabled", false).set("name", "hi"))));

        // Hidden is not a list
        assertThrows(Exception.class, () ->
            new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson()
                    .set("hidden", false)
                    .set("name", "hi"))));

        // actions is not a list
        assertThrows(Exception.class, () ->
            new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson()
                    .set("actions", false).set("name", "hu"))));

        // Require is not a list of strings
        assertThrows(Exception.class, () ->
            new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson()
                    .set("requires", false).set("name", "hi"))));
        assertThrows(Exception.class, () ->
            new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson()
                    .set("requires", AnyList.of(new AnyJson()))
                    .set("name", "hi"))));

        // Random key
        assertThrows(Exception.class, () ->
            new Upgrades().load(velvetDawn, "", AnyList.of(new AnyJson()
                    .set("random-key", AnyList.of("False"))
                    .set("name", "hi"))));

        // Valid
        new Upgrades().load(velvetDawn, "0", AnyList.of(new AnyJson()
                .set("id", "example")
                .set("enabled", AnyList.of(new AnyJson().set("if", "self").set("eq", "example")))
                .set("hidden", AnyList.of(new AnyJson().set("if", "self").set("ne", "example")))
                .set("actions", AnyList.of(new AnyJson().set("modify", "self.health").set("add", 1)))
                .set("requires", AnyList.of("eg"))
                .set("name", "hi")));
    }
}
