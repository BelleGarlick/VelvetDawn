package velvetdawn.core.models.config;

import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.utils.Path;

import java.util.List;

public class Config {

    public List<String> datapacks = List.of("civil-war");
    public SpawnConfig spawn = new SpawnConfig();
    public final MapConfig map = new MapConfig();
    public int setupTime = 300;
    public int turnTime = 300;
    public Integer seed = null;

    public Path getDatapackPath() {
        return new Path("../../datapacks");
    }

    public Path getWorldSavePath() {
        return new Path("../../worlds/world");
    }

    public void load(AnyJson data) throws Exception {
        this.spawn.load(data);
    }
}
