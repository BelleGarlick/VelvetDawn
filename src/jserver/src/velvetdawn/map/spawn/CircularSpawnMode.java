package velvetdawn.map.spawn;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.players.Player;

import java.util.Set;

public class CircularSpawnMode extends SpawnMode {

//    private Map<Coordinate> spawnPoints = Set.of();

    @Override
    public Set<Coordinate> getSpawnCoordinatesForPlayer(VelvetDawn velvetDawnCore, Config config, Player player) {
        return null;
    }

    @Override
    public void assignSpawnPoints(VelvetDawn velvetDawn, Config config) throws Exception {

    }
}
