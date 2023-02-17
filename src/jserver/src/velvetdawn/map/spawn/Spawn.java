package velvetdawn.map.spawn;

import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;
import velvetdawn.players.Player;

import java.util.Set;

public class Spawn {

    /* Spawn

    This module handles assigning spawnable tiles for players
    at the start of the game.

    When moving from the lobby to the setup phase, the allocate
    spawn points should be called to setup the the team's spawn
    areas
    */

    private final VelvetDawn velvetDawn;
    private final Config config;

    private final SpawnMode mode = new BorderSpawnMode();

    public Spawn(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;
    }

    public Set<Coordinate> getSpawnCoordinatesForPlayer(Player player) {
        return this.mode.getSpawnCoordinatesForPlayer(velvetDawn, config, player);
    }

    public boolean isPointSpawnable(Player player, Coordinate coordinate) {
        return this.mode.isPointSpawnable(velvetDawn, config, player, coordinate);
    }

    public void assignSpawnPoints() throws Exception {
        this.mode.assignSpawnPoints(this.velvetDawn, this.config);
    }
}
