package velvetdawn.game;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.GameSetup;
import velvetdawn.models.Phase;
import velvetdawn.models.instances.entities.EntityInstance;
import velvetdawn.players.Player;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.stream.Collectors;

public class Setup {

    /** velvet_dawn.game.setup
     *
     * This module handles the entity setup for the games. There
     * are functions for the admin to control the number of units
     * each player gets and if it's valid to start the game.
     *
     * This module also contains functions for the player to place
     * their initial setup entities when in the setup phase.
     */

    public Map<String, Integer> setup = new HashMap<>();

    private final VelvetDawn velvetDawn;

    public Setup(VelvetDawn velvetDawn) {
        this.velvetDawn = velvetDawn;
    }

    /** Get the game setup definition for a specific user */
    public GameSetup getSetup(Player player) {
        var commanderEntities = setup.keySet().stream()
                .filter(entityId -> velvetDawn.datapacks.entities.get(entityId).commander)
                .collect(Collectors.toSet());

        var entities = setup.keySet().stream()
                .filter(entityId -> !velvetDawn.datapacks.entities.get(entityId).commander)
                .collect(Collectors.toMap(entityId -> entityId, entityId -> setup.get(entityId)));

        // Calculate remaining units
        AtomicBoolean placedCommander = new AtomicBoolean(false);
        var remainingEntities = this.setup.keySet().stream()
                .collect(Collectors.toMap(key -> key, key -> this.setup.get(key)));

        player.entities.forEach(entity -> {
            if (commanderEntities.contains(entity.datapackId))
                placedCommander.set(true);
            else
                remainingEntities.put(entity.datapackId, remainingEntities.get(entity.datapackId) - 1);
        });

        return GameSetup
                .builder()
                .commanders(commanderEntities)
                .entities(entities)
                .commanderPlaced(placedCommander.get())
                .remainingEntities(remainingEntities)
                .build();
    }

    /** Update the initial entities a player may use. This
     * function should be called only be the admin during
     * the lobby phase.
     *
     * @param entityId The id of the entity to update the
     *                 count for
     * @param count The number of entities of this type
     *              a player may use. For commanders, this
     *              specific number will be ignored.
     */
    public void updateSetup(String entityId, Integer count) throws Exception {
        if (velvetDawn.game.phase != Phase.Lobby)
            throw new Exception("Game setup units may only be changed in the lobby by the admin");

        // Check entity exists
        if (!velvetDawn.datapacks.entities.containsKey(entityId))
            throw new Exception(String.format("Unknown entity id: '%s'", entityId));

        if (count == 0) {
            this.setup.remove(entityId);
        } else
            this.setup.put(entityId, count);
    }

    /** Check the setup definitions must contains commander and is
     * value for the game to start
     */
    public boolean isSetupValid() {
        // Filter out all non-commander units
        var commanderUnits = setup.keySet().stream()
                .filter(entityId -> {
                    return velvetDawn.datapacks.entities.get(entityId).commander
                            && setup.get(entityId) > 0;
                })
                .collect(Collectors.toSet());

        return !commanderUnits.isEmpty();
    }

    /** Place an entity in the world checking for setup constraints
     *
     * @param player Player placing the entity
     * @param entityId The entity id
     * @param position The position to place the entity.
     * @return The new entity instance.
     */
    public EntityInstance placeEntity(Player player, String entityId, Coordinate position) throws Exception {
        if (velvetDawn.game.phase != Phase.Setup)
            throw new Exception("Game setup may only be changed during game setup");

        var setup = this.getSetup(player);

        if (!velvetDawn.datapacks.entities.containsKey(entityId))
            throw new Exception("Unknown entity error");

        if (!velvetDawn.entities.getAtPosition(position).isEmpty())
            throw new Exception("Entity already exists in this tile.");

        if (!velvetDawn.map.spawn.isPointSpawnable(player, position))
            throw new Exception("This point is not within your spawn territory");

        if (!velvetDawn.map.isTraversable(position))
            throw new Exception("Entity cannot be placed here.");

        // Check that the entity is valid within the setup definition
        if (setup.getCommanders().contains(entityId)) {
            // Check they don't already have a commander
            if (setup.isCommanderPlaced())
                throw new Exception("You already have a commander in play");
        } else {
            var remainingEntities = setup.getRemainingEntities().get(entityId);
            if (remainingEntities == null)
                throw new Exception(String.format("Enitity %s not included in the setup definition.", entityId));

            if (remainingEntities < 0)
                throw new Exception(String.format("You already have the maximum number of %s in play", entityId));
        }

        // Spawn the entity
        return velvetDawn.entities.spawn(player, entityId, position);
    }

    /** Remove an entity from a cell
     *
     * @param position The position to remove the entity from
     */
    public void removeEntity(Player player, Coordinate position) throws Exception {
        if (velvetDawn.game.phase != Phase.Setup)
            throw new Exception("Game setup may only be changed during game setup");

        List<EntityInstance> entities = velvetDawn.entities.getAtPosition(position);
        if (entities.isEmpty())
            throw new Exception("No entity for you to remove here.");

        // TODO Filter for your own units

        for (EntityInstance entity: entities) {
            if (entity.player == player)
                velvetDawn.entities.remove(entity);
        }
    }

    /** This function checks all players have placed their commanders */
    public boolean validatePlayerSetups() {
        for (Player player: velvetDawn.players.listWithoutSpectators()) {
            AtomicBoolean playerHasCommander = new AtomicBoolean(false);

            player.entities.forEach(entityInstance -> {
                var entityDef = velvetDawn.datapacks.entities.get(entityInstance.datapackId);
                if (entityDef.commander)
                    playerHasCommander.set(true);
            });

            if (!playerHasCommander.get())
                return false;
        }

        return true;
    }

    public void save() {}
    public void load() {}
}
