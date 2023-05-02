package velvetdawn.core.game;

import velvetdawn.core.models.config.Config;
import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.Phase;
import velvetdawn.core.entities.EntityInstance;
import velvetdawn.core.models.instances.TileInstance;
import velvetdawn.core.models.instances.WorldInstance;

public class Game {

    public Phase phase = Phase.Lobby;

    public final Setup setup;
    public final Turns turns;

    private final VelvetDawn velvetDawn;

    public Game(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;

        this.setup = new Setup(velvetDawn);
        this.turns = new Turns(velvetDawn, config);
    }

    /** Start the setup phase in the game
     *
     * As part of this process the map will be generated
     * and the spawn points will be allocated.
     */
    public void startSetupPhase() throws Exception {
        System.out.println("Starting setup phase");
        velvetDawn.map.generate();
        this.turns.updateTurnStartTime();
        this.phase = Phase.Setup;

        // TODO Check game setup is valid before people start placing

        velvetDawn.players.list().forEach(player -> player.ready = false);
    }

    public void startGamePhase() throws Exception {
        this.phase = Phase.Game;

        // Trigger game start
        for (EntityInstance entity: velvetDawn.entities.list())
            velvetDawn.datapacks.entities.get(entity.datapackId).triggers.onGameStart(entity);

        for (TileInstance tile: velvetDawn.map.listTiles())
            velvetDawn.datapacks.tiles.get(tile.datapackId).triggers.onGameStart(tile);

        velvetDawn.datapacks.world.triggers.onGameStart(WorldInstance.getInstance());

        this.turns.beginNextTurn();

        // TODO if players haven't got a commander, move them to spectators

        // TODO Trigger entities on game start
        // TODO If game mode is CTF then trigger stuff here
    }

    public void save() {

    }

    public void load() {

    }
}
