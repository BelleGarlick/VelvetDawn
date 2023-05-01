package velvetdawn.core.mechanics.selectors;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.instances.Instance;

import java.util.Collection;
import java.util.stream.Collectors;

public class SelectorFriendlies extends Selector {

    /* Get the list of selectors who are on the same team / who's turn it is */

    public SelectorFriendlies(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        var playerBreakdown = velvetDawn.players.getFriendlyEnemyPlayersBreakdownForInstance(instance);
        Collection<Instance> entities = velvetDawn.entities.list().stream()
                .filter(x -> playerBreakdown.friendlyPlayers.contains(x.player))
                .collect(Collectors.toSet());

        return this.filters.filter(instance, entities);
    }
}
