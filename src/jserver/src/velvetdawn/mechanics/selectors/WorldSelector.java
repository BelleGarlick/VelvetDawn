package velvetdawn.mechanics.selectors;

import velvetdawn.VelvetDawn;
import velvetdawn.models.instances.Instance;
import velvetdawn.models.instances.WorldInstance;

import java.util.Collection;
import java.util.List;

public class WorldSelector extends Selector {

    /* Selector 'world' allows the user to access the world object
      in order to set/get attributes

      Some examples:
       - {"targets": "world.turns", "set": "5"}
       - {"targets": "world.players-count", "subtract": "2"}
     */

    public WorldSelector(VelvetDawn velvetDawn) { super(velvetDawn); }

    @Override
    protected Collection<Instance> getSelection(Instance instance) {
        return this.filters.filter(instance, List.of(WorldInstance.getInstance()));
    }
}
