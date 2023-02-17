package test;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;

import java.util.List;

public abstract class BaseTest {

    public Config getTestConfig() {
        Config config = new Config();
        config.datapacks = List.of("__testing__", "civil-war");
        return config;
    }

    public Config getConfig() {
        Config config = new Config();
        config.datapacks = List.of("__testing__");
        config.map.borderRadius = 5;
        config.map.seed = 0;
        config.spawn.spawnRadiusMultiplier = 1;
        config.spawn.baseSpawnRadius = 1;
        return config;
    }

    public VelvetDawn setupGame() throws Exception {
        Config config = this.getTestConfig();
        VelvetDawn velvetDawn = new VelvetDawn(config);
        velvetDawn.init();

        var p1 = velvetDawn.players.join("player1", "null");
        var p2 = velvetDawn.players.join("player2", "null");

        velvetDawn.game.setup.updateSetup("testing:commander", 1);
        velvetDawn.game.setup.updateSetup("civil-war:commander", 1);
        velvetDawn.game.setup.updateSetup("civil-war:cavalry", 1);
        velvetDawn.game.startSetupPhase();
        velvetDawn.game.setup.placeEntity(p1, "testing:commander", new Coordinate(15, 0));
        velvetDawn.game.setup.placeEntity(p1, "civil-war:cavalry", new Coordinate(14, 0));
        var instance = velvetDawn.game.setup.placeEntity(p2, "testing:commander", new Coordinate(15, config.map.borderRadius));
        velvetDawn.game.startGamePhase();

        velvetDawn.entities.move(instance, new Coordinate(15, 2));

        return velvetDawn;
    }

    public VelvetDawn prepareGame() throws Exception {
        Config config = this.getConfig();
        VelvetDawn velvetDawn = new VelvetDawn(config);
        velvetDawn.init();

        var p1 = velvetDawn.players.join("player1", "null");
        var p2 = velvetDawn.players.join("player2", "null");

        velvetDawn.game.setup.updateSetup("testing:commander", 1);
        velvetDawn.game.setup.updateSetup("testing:upgradable", 1);
        velvetDawn.game.setup.updateSetup("testing:abilitied", 1);
        velvetDawn.game.startSetupPhase();
        velvetDawn.game.setup.placeEntity(p1, "testing:commander", new Coordinate(0, -config.map.borderRadius));
        velvetDawn.game.setup.placeEntity(p1, "testing:upgradable", new Coordinate(-1, -config.map.borderRadius));
        velvetDawn.game.setup.placeEntity(p1, "testing:abilitied", new Coordinate(1, -config.map.borderRadius));
        var instance = velvetDawn.game.setup.placeEntity(p2, "testing:commander", new Coordinate(0, config.map.borderRadius));
        velvetDawn.game.startGamePhase();

        velvetDawn.entities.move(instance, new Coordinate(5, 2));

        return velvetDawn;
    }
}
