package velvetdawn.core.models;

import velvetdawn.core.players.Player;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Team {

    public String teamId;
    public String teamName;

    private List<Player> players = new ArrayList<>();

    public Team(String teamId, String teamName) {
        this.teamId = teamId;
        this.teamName = teamName;
    }

    public List<Player> listPlayersExcludeSpectators() {
        return players.stream().filter(player -> !player.spectating).collect(Collectors.toList());
    }

    public List<Player> listPlayers() {
        return players;
    }

    public void removePlayer(Player player) {
        this.players.remove(player);
    }

    public void addPlayer(Player player) {
        this.players.add(player);
    }
}
