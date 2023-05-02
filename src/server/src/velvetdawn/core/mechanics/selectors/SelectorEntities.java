package velvetdawn.core.mechanics.selectors;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.instances.Instance;

import java.util.Collection;

public class SelectorEntities extends Selector {

    /* Get all units in the game */

    public SelectorEntities(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        return this.filters.filter(instance, velvetDawn.entities.list());
    }
}
