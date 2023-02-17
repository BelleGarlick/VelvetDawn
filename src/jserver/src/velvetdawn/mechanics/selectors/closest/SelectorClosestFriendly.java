package velvetdawn.mechanics.selectors.closest;

import velvetdawn.VelvetDawn;
import velvetdawn.models.instances.Instance;

import java.util.Collection;
import java.util.stream.Collectors;

public class SelectorClosestFriendly extends SelectorClosestBase {

    /* Get the closest friendly to the given instance */

    public SelectorClosestFriendly(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        var playerBreakdown = velvetDawn.players.getFriendlyEnemyPlayersBreakdownForInstance(instance);
        Collection<Instance> entities = velvetDawn.entities.list().stream()
                .filter(x -> playerBreakdown.friendlyPlayers.contains(x.player))
                .collect(Collectors.toSet());

        return this.getClosest(instance, this.filters.filter(instance, entities));
    }
}
