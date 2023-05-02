package velvetdawn.core.mechanics.selectors.closest;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.instances.Instance;

import java.util.Collection;
import java.util.stream.Collectors;

public class SelectorClosestEnemy extends SelectorClosestBase {

    /* Get the closest enemy to the given instance */

    public SelectorClosestEnemy(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        var playerBreakdown = velvetDawn.players.getFriendlyEnemyPlayersBreakdownForInstance(instance);
        Collection<Instance> entities = velvetDawn.entities.list().stream()
                .filter(x -> playerBreakdown.enemyPlayers.contains(x.player))
                .collect(Collectors.toSet());

        return this.getClosest(instance, this.filters.filter(instance, entities));
    }
}
