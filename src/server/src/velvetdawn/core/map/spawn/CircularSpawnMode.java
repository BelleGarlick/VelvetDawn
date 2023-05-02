package velvetdawn.core.map.spawn;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.players.Player;

import java.util.List;
import java.util.Set;

public class CircularSpawnMode extends SpawnMode {

    public CircularSpawnMode(VelvetDawn velvetDawn, Config config) {
        super(velvetDawn, config);
    }

//    private Map<Coordinate> spawnPoints = Set.of();

    @Override
    public List<Coordinate> listAllSpawnPoints() {
        return null;
    }

    @Override
    public Set<Coordinate> getSpawnCoordinatesForPlayer(Player player) {
        return null;
    }

    @Override
    public void assignSpawnPoints() throws Exception {

    }
}
