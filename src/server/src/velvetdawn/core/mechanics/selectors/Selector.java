package velvetdawn.core.mechanics.selectors;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyFloat;
import velvetdawn.core.models.anytype.AnyNull;
import velvetdawn.core.models.anytype.AnyString;
import velvetdawn.core.models.instances.Instance;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;

public abstract class Selector {

    protected final VelvetDawn velvetDawn;

    public Filters filters;
    public Selector chainedSelector = null;
    public String attribute = null;

    public Selector(VelvetDawn velvetDawnCore) {
        this.velvetDawn = velvetDawnCore;
        this.filters = new Filters(velvetDawn);
    }

    protected abstract Collection<Instance> getSelection(Instance instance);

    public Collection<Instance> getChainedSelection(Instance instance) {
        var directSelection = this.getSelection(instance);
        if (this.chainedSelector == null)
            return directSelection;

        var chainedSelection = new HashSet<Instance>();
        directSelection.forEach(item -> {
            chainedSelection.addAll(this.chainedSelector.getChainedSelection(item));
        });

        return chainedSelection;
    }

    public void funcSet(Instance instance, Any value) {
        this.getChainedSelection(instance).forEach(item -> {
            item.attributes.set(this.attribute, value);
        });
    }

    public void funcAdd(Instance instance, Any value) {
        this.getChainedSelection(instance).forEach(item ->
                item.attributes.set(
                        this.attribute,
                        item.attributes.get(this.attribute).add(value)));
    }

    public void funcSub(Instance instance, Any value) {
        this.getChainedSelection(instance).forEach(item ->
                item.attributes.set(
                        this.attribute,
                        item.attributes.get(this.attribute).sub(value)));
    }

    public void funcMul(Instance instance, Any value) {
        this.getChainedSelection(instance).forEach(item ->
                item.attributes.set(
                        this.attribute,
                        item.attributes.get(this.attribute).mul(value)));
    }

    public void funcReset(Instance instance, Any value) {
        this.getChainedSelection(instance).forEach(item ->
                item.attributes.reset(this.attribute, value));
    }

    public void funcAddTag(Instance instance, Any tag) {
        this.getChainedSelection(instance).forEach(item -> item.tags.add(tag.toString()));
    }

    public void funcRemoveTag(Instance instance, Any tag) {
        this.getChainedSelection(instance).forEach(item -> item.tags.remove(tag.toString()));
    }

    /** Compare if the given value is equal the selectors' id / attribute value */
    public boolean funcEquals(Instance instance, Any value) {
        var instances = this.getChainedSelection(instance);
        if (instances.isEmpty())
            return false;

        for (Instance item: instances) {
            if (this.attribute != null) {
                if (!item.attributes.get(this.attribute).equals(value))
                    return false;
            } else if (!Objects.equals(item.datapackId, value.toString()))
                return false;
        }

        return true;
    }

    /** Compare if the entities attribute is less than a given value */
    public boolean funcLessThan(Instance instance, Any value) {
        var instances = this.getChainedSelection(instance);
        if (instances.isEmpty() || this.attribute == null)
            return false;

        for (Instance item: instances) {
            if (item.attributes.get(this.attribute).gte(value))
                return false;
        }

        return true;
    }

    /** Compare if the entities attribute is less/equal than a given value */
    public boolean funcLessThanEqual(Instance instance, Any value) {
        var instances = this.getChainedSelection(instance);
        if (instances.isEmpty() || this.attribute == null)
            return false;

        for (Instance item: instances) {
            if (item.attributes.get(this.attribute).gt(value))
                return false;
        }

        return true;
    }

    /** This function effectively works to get the mean value of the data */
    public Any funcGetValue(Instance instance) {
        var instances = this.getChainedSelection(instance);
        if (instances.isEmpty())
            return Any.Null();

        boolean allString = true;
        boolean allNumber = true;
        boolean allNull = true;
        String stringValue = null;
        List<Float> numberValues = new ArrayList<>();

        for (Instance item: instances) {
            Any value = this.attribute == null
                    ? new AnyString(item.datapackId)
                    : item.attributes.get(this.attribute);

            if (value instanceof AnyNull)
                continue;

            if (value instanceof AnyString) {
                allNumber = false;
                allNull = false;

                if (stringValue == null)
                    stringValue = value.toString();
                else if (!Objects.equals(stringValue, value.toString()))
                    return Any.Null();

            }
            else if (value instanceof AnyFloat) {
                allString = false;
                allNull = false;
                numberValues.add(value.toNumber());
            } else {
                // Invalid type
                return Any.Null();
            }
        }

        if (allNull)
            return Any.Null();

        if (allString)
            return new AnyString(stringValue);

        if (allNumber && !numberValues.isEmpty()) {
            float sum = 0;
            for (float v: numberValues)
                sum += v;
            return new AnyFloat(sum / ((float) numberValues.size()));
        }

        return Any.Null();
    }

    /** Check if the selection has a given tag */
    public boolean funcHasTag(Instance instance, Any tag) {
        var instances = this.getChainedSelection(instance);
        if (instances.isEmpty())
            return false;

        for (Instance item: instances) {
            if (!item.tags.contains(tag.toString()))
                return false;
        }

        return true;
    }
}
