package velvetdawn.mechanics.selectors.closest;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.selectors.Selector;
import velvetdawn.models.instances.EntityInstance;
import velvetdawn.models.instances.Instance;
import velvetdawn.models.instances.TileInstance;

import java.util.Collection;
import java.util.List;

public abstract class SelectorClosestBase extends Selector {

    public SelectorClosestBase(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    protected Collection<Instance> getClosest(Instance to, Collection<Instance> instances) {
        Instance closest = null;
        float bestDistance = 0;

        if (to instanceof TileInstance || to instanceof EntityInstance) {
            for (Instance item: instances) {
                // Don't want to include itself otherwise this will always return self
                if (item.instanceId.equals(to.instanceId) && to.getClass().equals(item.getClass()))
                    continue;

                int distance = velvetDawn.map.getDistance(to.position, item.position);

                if (closest == null) {
                    closest = item;
                    bestDistance = distance;
                } else if (distance < bestDistance) {
                    closest = item;
                    bestDistance = distance;
                }
            }
        }

        return closest == null
                ? List.of()
                : List.of(closest);
    }
}
