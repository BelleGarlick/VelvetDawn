package velvetdawn.core.mechanics.selectors;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.instances.Instance;

import java.util.Collection;
import java.util.List;

public class SelectorSelf extends Selector {

    /* Return the instance calling the selector */

    public SelectorSelf(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        return this.filters.filter(instance, List.of(instance));
    }
}
