package velvetdawn.core.map.spawn;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.players.Player;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class CentralSpawnMode extends SpawnMode {

    private Set<Coordinate> spawnPoints = Set.of();

    public CentralSpawnMode(VelvetDawn velvetDawn, Config config) {
        super(velvetDawn, config);
    }

    @Override
    public List<Coordinate> listAllSpawnPoints() {
        return new ArrayList<>(spawnPoints);
    }

    @Override
    public Set<Coordinate> getSpawnCoordinatesForPlayer(Player player) {
        return this.spawnPoints;
    }

    @Override
    public void assignSpawnPoints() {
        int spawnRadius = 1
                + config.spawn.baseSpawnRadius
                + (config.spawn.spawnRadiusMultiplier * velvetDawn.players.listWithoutSpectators().size());

        for (int i = 0; i < spawnRadius; i++) {
            Set<Coordinate> neighbours = new HashSet<>();
            this.spawnPoints.forEach(coord -> {
                neighbours.addAll(velvetDawn.map.getNeighbours(coord));
            });
            this.spawnPoints = neighbours;
        }
    }
}
