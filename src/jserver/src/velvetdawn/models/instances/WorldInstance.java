package velvetdawn.models.instances;

import velvetdawn.models.Coordinate;

public class WorldInstance extends Instance {

    private static WorldInstance instance = new WorldInstance();

    private WorldInstance() {
        super("world", "world", new Coordinate(0, 0));
    }

    public static WorldInstance getInstance() {
        return instance;
    }
}
