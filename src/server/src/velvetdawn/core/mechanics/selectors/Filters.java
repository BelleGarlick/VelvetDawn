package velvetdawn.core.mechanics.selectors;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.map.MapManager;
import velvetdawn.core.models.anytype.AnyFloat;
import velvetdawn.core.models.anytype.AnyString;
import velvetdawn.core.models.instances.TileInstance;
import velvetdawn.core.entities.EntityInstance;
import velvetdawn.core.models.instances.Instance;
import velvetdawn.core.models.instances.WorldInstance;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;
import java.util.stream.Collectors;

public class Filters {

    // TODO Add friendly/enemy filter
    // TODO Add not current turn/is current turn

    private final VelvetDawn velvetDawn;

    public final Set<String> allowedIds = new HashSet<>();
    public final Set<String> allowedTags = new HashSet<>();
    public Float minRange = null;
    public Float maxRange = null;
    public Integer random = null;
    public boolean excludeSelf = false;
    public boolean commanderOnly = false;
    public boolean closest = false;

    public Filters(VelvetDawn velvetDawn) {
        this.velvetDawn = velvetDawn;
    }

    public void addFilter(String key) throws Exception {
        this.addFilter(key, null);
    }

    /** Set a filter value */
    public void addFilter(String key, String value) throws Exception {
        switch (key) {
            case "id":
                this.allowedIds.add(value);
                break;
            case "exclude-self":
                this.excludeSelf = true;
                break;
            case "commander":
                this.commanderOnly = true;
                break;
            case "closest":
                this.closest = true;
                break;
            case "tag":
                this.allowedTags.add(value);
                break;
            case "range":
                this.maxRange = new AnyString(value)
                        .castToFloat()
                        .validateMinimum(0, "Range filter must be at least 0")
                        .value;
                break;
            case "min-range":
                this.minRange = new AnyString(value)
                        .castToFloat()
                        .validateMinimum(0, "Min-range filter must be at least 0")
                        .value;
                break;
            case "random":
                this.random = (int) new AnyString(value)
                        .castToFloat()
                        .validateMinimum(0, "Random filter must be at least 0")
                        .value;
                break;
            default:
                throw new Exception(String.format("Unknown filter: '%s'.", key));
        }
    }

    /** Filter the list of given instances from the perspective of the
     * given filter.
     *
     * Note, allowed tags are an 'and' clause but ids are an 'or' clause.
     *
     * @param instance The instance calling the selector which is filtering
     *                 the instances
     * @param instances The instances being filtered
     * @return The filtered instances
     */
    public Collection<Instance> filter(Instance instance, Collection<? extends Instance> instances) {
        List<Instance> filteredInstances = instances.stream()
                .filter(item -> {
                    // If missing tag, filter out the item
                    if (!this.allowedTags.isEmpty()) {
                        for (String tag: this.allowedTags) {
                            if (!item.tags.contains(tag))
                                return false;
                        }
                    }

                    // Check the id is in the list of given tags
                    if (!this.allowedIds.isEmpty()) {
                        if (!this.allowedIds.contains(item.datapackId))
                            return false;
                    }

                    // Check the max range if not world instance
                    if (this.maxRange != null) {
                        if (item instanceof WorldInstance)
                            return false;
                        else {
                            int distance = MapManager.getDistance(instance.position, item.position);
                            if (distance > this.maxRange)
                                return false;
                        }
                    }

                    // Check the min range if not world instance
                    if (this.minRange != null) {
                        if (item instanceof WorldInstance)
                            return false;
                        else {
                            int distance = MapManager.getDistance(instance.position, item.position);
                            if (distance < this.minRange)
                                return false;
                        }
                    }

                    if (this.excludeSelf) {
                        if (instance.instanceId.equals(item.instanceId)
                                && instance.getClass().equals(item.getClass()))
                            return false;
                    }

                    if (this.commanderOnly) {
                        if (item instanceof EntityInstance) {
                            if (!velvetDawn.datapacks.entities.get(item.datapackId).commander)
                                return false; // Is not comander
                        } else
                            return false; // if commander is specified then only entities are valid
                    }

                    // No prev condition met, don't filter out th item
                    return true;
                })
                .collect(Collectors.toList());

        // If there is a random value and it's smaller than the sample.
        // We compare the sample size since we don't want to repeat instances
        if (this.random != null && this.random < filteredInstances.size()) {
            // Create list of indexes and shuffle
            var indexes = new ArrayList<Integer>();
            for (int i = 0; i < filteredInstances.size(); i++)
                indexes.add(i);
            Collections.shuffle(indexes);

            // Sample from items
            var randomItems = new ArrayList<Instance>(this.random);
            for (int i = 0; i < this.random; i++)
                randomItems.add(filteredInstances.get(indexes.get(i)));
            filteredInstances = randomItems;
        }

        if (this.closest)
            filteredInstances = getClosest(instance, filteredInstances);

        return filteredInstances;
    }

    private List<Instance> getClosest(Instance to, List<Instance> instances) {
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
