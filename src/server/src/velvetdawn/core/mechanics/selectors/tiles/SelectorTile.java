package velvetdawn.core.mechanics.selectors.tiles;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.mechanics.selectors.Selector;
import velvetdawn.core.entities.EntityInstance;
import velvetdawn.core.models.instances.Instance;
import velvetdawn.core.models.instances.TileInstance;

import java.util.Collection;
import java.util.List;

public class SelectorTile extends Selector {

    /* Get the tile of the position of the given instance */

    public SelectorTile(VelvetDawn velvetDawn) {
        super(velvetDawn);
    }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        if (instance instanceof TileInstance)
            return this.filters.filter(instance, List.of(instance));

        if (instance instanceof EntityInstance) {
            var tile = velvetDawn.map.getTile(instance.position);
            if (tile != null)
                return this.filters.filter(instance, List.of(tile));

            return this.filters.filter(instance, List.of());
        }

        return List.of();
    }
}
