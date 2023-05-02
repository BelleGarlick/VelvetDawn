package velvetdawn.server.models;

import lombok.Builder;

import java.util.List;
import java.util.stream.Collectors;

import velvetdawn.core.models.Team;

@Builder
public class APITeam {

    public String id;
    public String name;
    public List<String> players;

    public static APITeam fromTeam(Team team) {
        return APITeam.builder()
                .id(team.teamId)
                .name(team.teamName)
                .players(team.listPlayers()
                        .stream()
                        .map(p -> p.name)
                        .collect(Collectors.toList()))
                .build();
    }

    public static List<APITeam> fromTeams(List<Team> teams) {
        return teams
                .stream()
                .map(APITeam::fromTeam)
                .collect(Collectors.toList());
    }
}
