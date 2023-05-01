package velvetdawn.core.models.config;

import velvetdawn.core.models.anytype.AnyFloat;
import velvetdawn.core.models.anytype.AnyJson;

import java.util.Random;

public class MapConfig {

    public int seed = -1;
    public int width = 29;
    public int height = 19;

    /** Parse the spawn mode json */
    public void load(AnyJson configJson) throws Exception {
        var mapConfig = configJson.get("map", new AnyJson())
                .validateInstanceIsJson("Config 'map' must be a json object.");

        Random random = new Random();
        this.seed = (int) mapConfig
                .get("seed", new AnyFloat(random.nextInt()))
                .validateInstanceIsFloat("Map seed must be a number").value;

        this.width = (int) mapConfig
                .get("width", new AnyFloat(29))
                .validateInstanceIsFloat("Map width must be a number")
                .validateMinimum(0, "Map width must be at least 0").value;

        this.height = (int) mapConfig
                .get("height", new AnyFloat(19))
                .validateInstanceIsFloat("Map height must be a number")
                .validateMinimum(0, "Map height must be at least 0").value;
    }
}
