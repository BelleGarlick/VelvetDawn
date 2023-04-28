package velvetdawn.map.spawn;

import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;
import velvetdawn.players.Player;

import java.util.List;
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

    private final SpawnMode mode;

    public Spawn(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;

        switch (this.config.spawn.mode) {
            case Random: {
                this.mode = new RandomSpawnMode(velvetDawn, config);
                break;
            }
            case Central: {
                this.mode = new CentralSpawnMode(velvetDawn, config);
                break;
            }
            case Boundary: {
                this.mode = new BorderSpawnMode(velvetDawn, config);
                break;
            }
            case Circular: {
                this.mode = new CircularSpawnMode(velvetDawn, config);
                break;
            }
            default: {
                this.mode = new BorderSpawnMode(velvetDawn, config);
            }
        }
    }

    public Set<Coordinate> getSpawnCoordinatesForPlayer(Player player) {
        return this.mode.getSpawnCoordinatesForPlayer(player);
    }

    public boolean isPointSpawnable(Player player, Coordinate coordinate) {
        return this.mode.isPointSpawnable(player, coordinate);
    }

    public void assignSpawnPoints() throws Exception {
        this.mode.assignSpawnPoints();
    }

    public List<Coordinate> listAllSpawnPoints() {
        return this.mode.listAllSpawnPoints();
    }
}
