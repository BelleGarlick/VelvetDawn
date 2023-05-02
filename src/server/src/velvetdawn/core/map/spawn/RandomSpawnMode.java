package velvetdawn.core.map.spawn;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.players.Player;

import java.util.List;
import java.util.Set;

// TODO Also create a distributed models

public class RandomSpawnMode extends SpawnMode {

    public RandomSpawnMode(VelvetDawn velvetDawn, Config config) {
        super(velvetDawn, config);
    }

    @Override
    public List<Coordinate> listAllSpawnPoints() {
        return null;
    }

    @Override
    public Set<Coordinate> getSpawnCoordinatesForPlayer(Player player) {
        // todo assign
        return null;
    }

    /** Spawn points are only assigned upon request for this mode */
    @Override
    public void assignSpawnPoints() {}
}
