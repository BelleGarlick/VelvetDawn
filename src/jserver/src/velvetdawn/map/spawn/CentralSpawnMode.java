package velvetdawn.map.spawn;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.players.Player;

import java.util.HashSet;
import java.util.Set;

public class CentralSpawnMode extends SpawnMode {

    private Set<Coordinate> spawnPoints = Set.of();

    @Override
    public Set<Coordinate> getSpawnCoordinatesForPlayer(VelvetDawn velvetDawnCore, Config config, Player player) {
        return this.spawnPoints;
    }

    @Override
    public void assignSpawnPoints(VelvetDawn velvetDawn, Config config) {
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
