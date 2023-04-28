package velvetdawn.map.spawn;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.players.Player;

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
