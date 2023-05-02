package velvetdawn.core.entities;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.instances.entities.EntityInstance;
import velvetdawn.core.models.instances.entities.EntityInstanceUpdate;
import velvetdawn.core.players.Player;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

public class EntityManager {

    private static final List<EntityInstanceUpdate> updates = new ArrayList<>();
    private static final List<EntityInstanceUpdate> deaths = new ArrayList<>();
    private static final long EntityBroadcastTTL = 10 * 1000;

    private final VelvetDawn velvetDawn;

    private final Set<EntityInstance> entities = new HashSet<>();

    public final Movement movement;

    public EntityManager(VelvetDawn velvetDawn) {
        this.velvetDawn = velvetDawn;
        this.movement = new Movement(velvetDawn);
    }

    public List<EntityInstance> list() {
        return new ArrayList<>(this.entities);
    }

    /** Spawn an entity
     *
     * @param player Player who owns the entity
     * @param entityId The datapack id of the entity
     * @param position The position of the entity
     */
    public EntityInstance spawn(Player player, String entityId, Coordinate position) throws Exception {
        if (!velvetDawn.datapacks.entities.containsKey(entityId))
            throw new Exception(String.format("Unknown entity Id %s", entityId));

        var definition = velvetDawn.datapacks.entities.get(entityId);

        var entity = new EntityInstance(
                velvetDawn,
                player,
                UUID.randomUUID().toString(),
                entityId,
                position
        );

        // Update entity before spawning
        entity.tags.addAll(definition.tags);
        definition.attributes.attributes.forEach(item ->
            entity.attributes.set(item.id, item.value));

        // Store new data
        player.entities.add(entity);
        this.entities.add(entity);

        // Trigger on spawn
        definition.triggers.onSpawn(entity);

        // Add to updates
        updates.add(EntityInstanceUpdate.from(entity));

        return entity;
    }

    public void kill(EntityInstance entity) {
        this.entities.remove(entity);
        entity.player.entities.remove(entity);
        deaths.add(EntityInstanceUpdate.from(entity));
    }

    public void removeForPlayer(Player player) {
        player.entities.forEach(this.entities::remove);
        player.entities.clear();
    }

    public void remove(EntityInstance entity) {
        this.entities.remove(entity);
        entity.player.entities.remove(entity);
    }

    public List<EntityInstanceUpdate> getUpdatesBroadcast(boolean fullState) {
        // TODO Needs testing as does attr update
        if (fullState)
            return this.entities.stream().map(EntityInstanceUpdate::from).collect(Collectors.toList());

        long now = System.currentTimeMillis() - EntityBroadcastTTL;
        while (!updates.isEmpty()) {
            if (updates.get(0).time < now)
                updates.remove(0);
            else
                break;
        }
        return updates;
    }

    public List<String> getRemovalsBroadcast() {
        while (!deaths.isEmpty()) {
            if (deaths.get(0).time < System.currentTimeMillis() - EntityBroadcastTTL)
                deaths.remove(0);
            else
                break;
        }

        return deaths.stream().map(x -> x.instanceId).collect(Collectors.toList());
    }

    public List<EntityInstance> getAtPosition(Coordinate position) {
        // TODO Optimise
        return this.entities.stream().filter(entityInstance -> entityInstance.position.tileEquals(position)).collect(Collectors.toList());
    }

    public void setPosition(EntityInstance instance, Coordinate coordinate) {
        // TODO Store in map - remove item from map
        instance.position = coordinate;
        updates.add(EntityInstanceUpdate.from(instance));
        // TODO Store in map - add item to new position in hashmap
    }

    public Set<EntityInstance> all() {
        return this.entities;
    }

    public EntityInstance getById(String instanceId) {
        for (EntityInstance instance: this.entities) {
            if (instance.instanceId.equals(instanceId))
                return instance;
        }

        return null;
    }
}
