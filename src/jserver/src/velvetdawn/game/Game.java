package velvetdawn.game;

import velvetdawn.models.Coordinate;
import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;
import velvetdawn.models.GameState;
import velvetdawn.models.Phase;
import velvetdawn.models.instances.entities.EntityInstance;
import velvetdawn.models.instances.TileInstance;
import velvetdawn.models.instances.WorldInstance;
import velvetdawn.players.Player;

import java.util.Set;

public class Game {

    public Phase phase = Phase.Lobby;

    public final Setup setup;
    public final Turns turns;

    private final VelvetDawn velvetDawn;
    private final Config config;

    public Game(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;

        this.setup = new Setup(velvetDawn);
        this.turns = new Turns(velvetDawn, config);
    }

    /** Get the update state of the game
     *
     * @param velvetDawn VelvetDawn object
     * @param config The game config
     * @param player The player requesting the update
     * @param fullState Whether the player wants the full state
     * @return The game state
     */
    public GameState getState(VelvetDawn velvetDawn, Config config, Player player, boolean fullState) {
        Set<Coordinate> spawnPoints = this.phase == Phase.Setup
                ? velvetDawn.map.spawn.getSpawnCoordinatesForPlayer(player)
                : Set.of();

        return GameState.builder()
                .phase(this.phase)
                .setup(this.setup.getSetup(player))
                .turnData(this.turns.currentTurnData())
                .teams(velvetDawn.teams.list())
                .players(velvetDawn.players.list())
                .entityChanges(velvetDawn.entities.getUpdatesBroadcast(fullState))
                .tileChanges(velvetDawn.map.getUpdatesBroadcast(fullState))
                .spawnArea(spawnPoints)
                .build();
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
