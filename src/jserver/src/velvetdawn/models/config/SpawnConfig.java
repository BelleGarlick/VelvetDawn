package velvetdawn.models.config;

import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.utils.Json;

public class SpawnConfig {

    public enum SpawnMode {
        Boundary,
        Central,
        Random
    }

    public SpawnMode mode = SpawnMode.Central;
    public int baseSpawnRadius = 5;
    public int spawnRadiusMultiplier = 0;

    /** Parse the spawn mode json */
    public void load(Json configJson) throws Exception {
        var spawnConfig = configJson.getJson("spawn", new Json(), "Config 'spawn' must be a json object.");

        var spawnMode = spawnConfig.get("move")
                .validateInstanceIsStringOrNull("Spawn mode 'move' must be a string or null");
        if (spawnMode != null) {
            switch (spawnMode.toString()) {
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
