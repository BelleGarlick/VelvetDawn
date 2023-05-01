package velvetdawn.server.models;

import com.google.gson.JsonObject;
import velvetdawn.core.models.GameSetup;
import velvetdawn.core.models.Phase;
import velvetdawn.core.models.Team;
import velvetdawn.core.models.TurnData;
import velvetdawn.core.models.instances.TileInstanceUpdate;
import velvetdawn.core.models.instances.entities.EntityInstanceUpdate;
import velvetdawn.core.players.Player;
import velvetdawn.server.VelvetDawnServerInstance;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

public class GameState {

    public Phase phase;
    public List<JsonObject> spawnArea;
    public TurnData turnData;

    public Collection<Player> players;
    public List<Team> teams;

    public List<EntityInstanceUpdate> entityChanges;
    public List<TileInstanceUpdate> tileChanges;

    public JsonObject setup;

    public static GameState from(Player player) {
        var velvetDawn = VelvetDawnServerInstance.getInstance();

        var gameState = new GameState();
        gameState.phase = velvetDawn.game.phase;
        gameState.spawnArea = velvetDawn.game.phase == Phase.Setup
                ? velvetDawn.map.spawn.getSpawnCoordinatesForPlayer(player).stream()
                    .map(coord -> coord.json().toGson())
                    .collect(Collectors.toList())
                : List.of();
        gameState.setup = velvetDawn.game.setup.getSetup(player).json().toGson();


//        /** Get the update state of the game
//         *
//         * @param velvetDawn VelvetDawn object
//         * @param config The game config
//         * @param player The player requesting the update
//         * @param fullState Whether the player wants the full state
//         * @return The game state
//         */
//        public GameState getState(VelvetDawn velvetDawn, Config config, Player player, boolean fullState) {
//            Set<Coordinate> spawnPoints = this.phase == Phase.Setup
//                    ? velvetDawn.map.spawn.getSpawnCoordinatesForPlayer(player)
//                    : Set.of();
//
//            return GameState.builder()
//                    .phase(this.phase)
//                    .setup(this.setup.getSetup(player))
//                    .turnData(this.turns.currentTurnData())
//                    .teams(velvetDawn.teams.list())
//                    .players(velvetDawn.players.list())
//                    .entityChanges(velvetDawn.entities.getUpdatesBroadcast(fullState))
//                    .tileChanges(velvetDawn.map.getUpdatesBroadcast(fullState))
//                    .spawnArea(spawnPoints)
//                    .build();
//        }

        return gameState;
    }
}
