package velvetdawn.server;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.config.Config;

public class VelvetDawnServerInstance {

    private static VelvetDawn velvetDawn;

    public static VelvetDawn getInstance() {
        return velvetDawn;
    }

    public static void init() throws Exception {
        Config config = new Config();
        config.spawn.spawnRadiusMultiplier = 2;
        config.spawn.baseSpawnRadius = 2;
        VelvetDawnServerInstance.velvetDawn = new VelvetDawn(config);
    }
}
