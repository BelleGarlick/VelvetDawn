package velvetdawn.models.config;

import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.utils.Json;

import java.util.Random;

public class MapConfig {

    public int seed = -1;
    public int borderRadius = 300_000;

    /** Parse the spawn mode json */
    public void load(Json configJson) throws Exception {
        var mapConfig = configJson.getJson("map", new Json(), "Config 'map' must be a json object.");

        Random random = new Random();
        this.seed = (int) mapConfig
                .get("seed", new AnyFloat(random.nextInt()))
                .validateInstanceIsFloat("Map seed must be a number").value;

        this.borderRadius = (int) mapConfig
                .get("radius", new AnyFloat(300_000))
                .validateInstanceIsFloat("Map radius must be a number")
                .validateMinimum(0, "Map radius must be at least 0").value;
    }
}
