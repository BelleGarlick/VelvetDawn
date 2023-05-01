package velvetdawn.core.mechanics.selectors;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.instances.entities.EntityInstance;
import velvetdawn.core.models.instances.Instance;
import velvetdawn.core.models.instances.TileInstance;

import java.util.Collection;
import java.util.List;

public class SelectorUnit extends Selector {

    /* Get a single unit in the same position as the given instance */

    public SelectorUnit(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        if (instance instanceof EntityInstance)
            return this.filters.filter(instance, List.of(instance));

        if (instance instanceof TileInstance) {
            return this.filters.filter(
                    instance,
                    velvetDawn.map.getEntitiesAtPosition(((TileInstance) instance).position));
        }

        return List.of();
    }
}
