package velvetdawn.core.teams;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.Phase;
import velvetdawn.core.models.Team;
import velvetdawn.core.players.Player;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class TeamsManager {

    private final VelvetDawn velvetDawn;

    private final ArrayList<Team> teams = new ArrayList<>();

    public TeamsManager(VelvetDawn velvetDawn) {
        this.velvetDawn = velvetDawn;
    }

    public List<Team> list() {
        return this.teams;
    }

    public List<Team> listWithoutSpectators() {
        return this.teams.stream()
                .filter(team -> team.listPlayersExcludeSpectators().size() > 0)
                .collect(Collectors.toList());
    }

    public int maxTeamSizeWithoutSpectators() {
        var max = 0;
        for (Team team: this.teams)
            max = Math.max(max, team.listPlayersExcludeSpectators().size());
        return max;
    }

    private void removeEmptyTeams() {
        List<Team> teams = new ArrayList<>();
        for (Team team: this.teams) {
            if (team.listPlayers().isEmpty())
                teams.add(team);
        }

        teams.forEach(this.teams::remove);
    }

    private Team newTeam(String teamId, String teamName) {
        var team = new Team(teamId, teamName);
        this.teams.add(team);
        return team;
    }

    private void addPlayerToTeam(Team team, Player player) {
        if (player.team != null) {
            player.team.removePlayer(player);
        }

        team.addPlayer(player);
        player.team = team;
    }

    public void autoUpdate() {
        System.out.println("Updating teams");
        var players = velvetDawn.players.list().stream()
                .filter(player -> player.team == null)
                .collect(Collectors.toList());

        // If in game, add player to the spectators team
        if (velvetDawn.game.phase != Phase.Lobby) {
            players.forEach(player -> {
                player.spectating = true;
            });
        }

        players.forEach(player -> {
            System.out.println(String.format("Adding %s to their own team", player.name));
            addPlayerToTeam(
                    newTeam(
                            String.format("team:%s", player.name),
                            player.name
                    ),
                    player
            );
        });

        this.removeEmptyTeams();
    }
}
