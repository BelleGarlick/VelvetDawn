package velvetdawn.core.models.instances;

import velvetdawn.core.models.Coordinate;

public class WorldInstance extends Instance {

    private static final WorldInstance instance = new WorldInstance();

    private WorldInstance() {
        super("world", "world", new Coordinate(0, 0));
    }

    public static WorldInstance getInstance() {
        return instance;
    }
}
