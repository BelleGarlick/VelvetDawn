package velvetdawn.models;

import lombok.Builder;
import velvetdawn.models.instances.entities.EntityInstanceUpdate;
import velvetdawn.models.instances.TileInstanceUpdate;
import velvetdawn.players.Player;

import java.util.Collection;
import java.util.List;
import java.util.Set;

@Builder
public class GameState {

    // TODO Change teams and player only to the updates

    private Phase phase;
    private Set<Coordinate> spawnArea;
    private TurnData turnData;

    private Collection<Player> players;
    private List<Team> teams;

    private List<EntityInstanceUpdate> entityChanges;
    private List<TileInstanceUpdate> tileChanges;

    private GameSetup setup;
}
