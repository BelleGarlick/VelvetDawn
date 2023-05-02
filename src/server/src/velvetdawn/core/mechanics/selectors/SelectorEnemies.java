package velvetdawn.core.mechanics.selectors;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.instances.Instance;

import java.util.Collection;
import java.util.stream.Collectors;

public class SelectorEnemies extends Selector {

    /* Get the list of selectors who are not on the same team / who's turn it is not */

    public SelectorEnemies(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        var playerBreakdown = velvetDawn.players.getFriendlyEnemyPlayersBreakdownForInstance(instance);
        Collection<Instance> entities = velvetDawn.entities.list().stream()
                .filter(x -> playerBreakdown.enemyPlayers.contains(x.player))
                .collect(Collectors.toSet());

        return this.filters.filter(instance, entities);
    }
}
