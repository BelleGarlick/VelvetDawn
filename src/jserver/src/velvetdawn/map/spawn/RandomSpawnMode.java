package velvetdawn.map.spawn;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.players.Player;

import java.util.Set;

public class RandomSpawnMode extends SpawnMode {

    @Override
    public Set<Coordinate> getSpawnCoordinatesForPlayer(VelvetDawn velvetDawnCore, Config config, Player player) {
        // todo assign
        return null;
    }

    /** Spawn points are only assigned upon request for this mode */
    @Override
    public void assignSpawnPoints(VelvetDawn velvetDawn, Config config) {}
}
