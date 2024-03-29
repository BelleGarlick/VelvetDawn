package velvetdawn.core.map.spawn;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.players.Player;

import java.util.List;
import java.util.Set;

public abstract class SpawnMode {

    protected final VelvetDawn velvetDawn;
    protected final Config config;

    public SpawnMode(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;
    }

    public abstract List<Coordinate> listAllSpawnPoints();

    public abstract Set<Coordinate> getSpawnCoordinatesForPlayer(Player player);

    /** Check if the given point exists within the player's spawn territory */
    public boolean isPointSpawnable(Player player, Coordinate coordinate) {
        return this
                .getSpawnCoordinatesForPlayer(player)
                .stream()
                .anyMatch(coord -> coord.tileEquals(coordinate));
    }

    public abstract void assignSpawnPoints() throws Exception;
}
