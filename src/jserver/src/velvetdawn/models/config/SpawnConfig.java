package velvetdawn.models.config;

import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.models.anytype.AnyJson;

public class SpawnConfig {

    public enum SpawnMode {
        Boundary,
        Central,
        Random,
        Circular
    }

    public SpawnMode mode = SpawnMode.Boundary;
    public int baseSpawnRadius = 5;
    public int spawnRadiusMultiplier = 0;

    public SpawnConfig() {}
    public SpawnConfig(SpawnMode mode, int baseSpawnRadius, int spawnRadiusMultiplier) {
        this.mode = mode;
        this.baseSpawnRadius = baseSpawnRadius;
        this.spawnRadiusMultiplier = spawnRadiusMultiplier;
    }

    /** Parse the spawn mode json */
    public void load(AnyJson configJson) throws Exception {
        var spawnConfig = configJson
                .get("spawn", new AnyJson())
                .validateInstanceIsJson("Config 'spawn' must be a json object.");

        String spawnMode = null;
        if (spawnConfig.containsKey("mode"))
            spawnMode = spawnConfig
                    .get("mode")
                    .validateInstanceIsString("Spawn mode 'move' must be a string")
                    .value;
        if (spawnMode != null) {
            switch (spawnMode) {
                case "boundary": {
                    this.mode = SpawnMode.Boundary;
                    break;
                }
                case "random": {
                    this.mode = SpawnMode.Random;
                    break;
                }
                default: {
                    this.mode = SpawnMode.Central;
                    break;
                }
            }
        }

        this.baseSpawnRadius = (int) spawnConfig
                .get("radius", new AnyFloat(5))
                .validateInstanceIsFloat("Spawn radius must be a number")
                .validateMinimum(0, "Spawn radius must be at least 0").value;

        this.spawnRadiusMultiplier = (int) spawnConfig
                .get("multiplier", new AnyFloat(0))
                .validateInstanceIsFloat("Spawn radius multipier must be a number")
                .validateMinimum(0, "Spawn multipier must be at least 0").value;
    }
}
