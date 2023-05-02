package velvetdawn.server.models;

import lombok.Builder;
import velvetdawn.core.players.Player;
import velvetdawn.server.VelvetDawnServerInstance;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

@Builder
public class APIPlayer {

    public String name;
    public boolean admin;

    public boolean ready;
    public boolean spectating;

    public String team;

    public static APIPlayer fromPlayer(Player player) {
        return APIPlayer.builder()
                .name(player.name)
                .admin(player.admin)
                .ready(player.ready)
                .spectating(player.spectating)
                .team(player.team != null ? player.team.teamId : null)
                .build();
    }

    public static List<APIPlayer> fromPlayers(Collection<Player> players) {
        return players
                .stream()
                .map(APIPlayer::fromPlayer)
                .collect(Collectors.toList());
    }
}
