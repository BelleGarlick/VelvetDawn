package velvetdawn.mechanics.actions;

import velvetdawn.mechanics.conditionals.Conditional;
import velvetdawn.models.instances.Instance;

import java.util.ArrayList;
import java.util.List;

public abstract class Action {

    /* Abstract base action class

    All other actions should derive from this class
    */

    private final List<Conditional> conditions = new ArrayList<>();

    public void addCondition(Conditional condition) {
        this.conditions.add(condition);
    }

    /** Execute the action */
    public abstract void run(Instance instance) throws Exception;

    /** Test if the action can run */
    public boolean canRun(Instance instance) {
        for (Conditional condition: this.conditions) {
            if (!condition.isTrue(instance))
                return false;
        }
        return true;
    }

}
