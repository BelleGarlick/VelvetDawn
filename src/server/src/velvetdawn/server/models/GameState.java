package velvetdawn.server.models;

import com.google.gson.JsonObject;
import lombok.Builder;
import velvetdawn.core.models.Phase;
import velvetdawn.core.models.instances.attributes.Attributes;
import velvetdawn.core.players.Player;
import velvetdawn.server.VelvetDawnServerInstance;

import java.util.List;
import java.util.stream.Collectors;

@Builder
public class GameState {

    public Phase phase;
    public List<APICoordinate> spawnArea;
    public APITurnData turn;

    public List<APIPlayer> players;
    public List<APITeam> teams;

    public List<APIEntityUpdate> entityUpdates;
    public List<String> entityRemovals;
    public List<JsonObject> attributeUpdates;

    public APIGameSetup setup;

    public APIMapResponse map;

    public static GameState from(Player player) {
        return GameState.from(player, false);
    }

    public static GameState from(Player player, boolean fullState) {
        var velvetDawn = VelvetDawnServerInstance.getInstance();

        List<APICoordinate> spawnArea = velvetDawn.game.phase == Phase.Setup
                ? velvetDawn.map.spawn.getSpawnCoordinatesForPlayer(player).stream()
                .map(APICoordinate::fromCoordinate)
                .collect(Collectors.toList())
                : List.of();

        return GameState.builder()
                .phase(velvetDawn.game.phase)
                .spawnArea(spawnArea)
                .setup(APIGameSetup.from(player))
                .teams(APITeam.fromTeams(velvetDawn.teams.list()))
                .players(APIPlayer.fromPlayers(velvetDawn.players.list()))
                .entityUpdates(APIEntityUpdate.fromUpdates(velvetDawn.entities.getUpdatesBroadcast(fullState)))
                .entityRemovals(velvetDawn.entities.getRemovalsBroadcast())
                .attributeUpdates(APIAttributeUpdate.fromUpdates(Attributes.getUpdates(velvetDawn, fullState)))
                .turn(new APITurnData())
                .map(fullState ? new APIMapResponse() : null)
                .build();
    }
}
