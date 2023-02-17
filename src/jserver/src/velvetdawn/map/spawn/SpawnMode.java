package velvetdawn.map.spawn;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.players.Player;

import java.util.Set;

public abstract class SpawnMode {

    public abstract Set<Coordinate> getSpawnCoordinatesForPlayer(VelvetDawn velvetDawnCore, Config config, Player player);

    /** Check if the given point exists within the player's spawn territory */
    public boolean isPointSpawnable(VelvetDawn velvetDawnCore, Config config, Player player, Coordinate coordinate) {
        Set<Coordinate> spawnPoints = this.getSpawnCoordinatesForPlayer(velvetDawnCore, config, player);

        boolean valid = false;
        for (Coordinate coord: spawnPoints)
            valid = valid || coord.equals(coordinate);

        return valid;
    }

    public abstract void assignSpawnPoints(VelvetDawn velvetDawn, Config config) throws Exception;
}
