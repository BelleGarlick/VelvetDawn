package velvetdawn.entities;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.instances.EntityInstance;
import velvetdawn.models.instances.EntityInstanceUpdate;
import velvetdawn.players.Player;

import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

public class EntityManager {

    private final Set<EntityInstance> entities = new HashSet<>();

    private final VelvetDawn velvetDawn;
    private final Movement movement = new Movement();

    public EntityManager(VelvetDawn velvetDawn) {
        this.velvetDawn = velvetDawn;
    }

    public Collection<EntityInstance> list() {
        return this.entities;
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

        var entity = new EntityInstance(
                player,
                UUID.randomUUID().toString(),
                entityId,
                position
        );

        player.entities.add(entity);
        this.entities.add(entity);

        return entity;
    }

    public void kill(EntityInstance entity) {
        this.entities.remove(entity);
        entity.player.entities.remove(entity);
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
        // todo needs implementing
        return List.of();
    }

    public List<EntityInstance> getAtPosition(Coordinate position) {
        // TODO Optimise
        return this.entities.stream().filter(entityInstance -> {
            return entityInstance.position.tileX() != position.tileX() || entityInstance.position.tileY() != position.tileY();
        }).collect(Collectors.toList());
    }

    public void move(EntityInstance instance, Coordinate coordinate) {
        this.movement.move(instance, coordinate);
    }
}
