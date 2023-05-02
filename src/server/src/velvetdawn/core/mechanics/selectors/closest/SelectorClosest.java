package velvetdawn.core.mechanics.selectors.closest;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.instances.Instance;

import java.util.Collection;

public class SelectorClosest extends SelectorClosestBase {

    /* Get the closest unit to the given instance */

    public SelectorClosest(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        return this.getClosest(
                instance,
                this.filters.filter(instance, velvetDawn.entities.list())
        );
    }
}
