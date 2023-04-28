package velvetdawn.entities;

import velvetdawn.VelvetDawn;
import velvetdawn.constants.AttributeKeys;
import velvetdawn.models.Coordinate;
import velvetdawn.models.Phase;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.instances.TileInstance;
import velvetdawn.models.instances.entities.EntityInstance;

import java.util.List;
import java.util.stream.Collectors;

public class Movement {

    private final VelvetDawn velvetDawn;

    public Movement(VelvetDawn velvetDawn) {
        this.velvetDawn = velvetDawn;
    }

    public int getRemainingMoves(EntityInstance entity) {
        return (int) entity.attributes.get(AttributeKeys.EntityRemainingMoves, Any.from(0)).toNumber();
    }

    /** Move an entity along a path
     * 
     * @param entity The entity to move
     * @param path The path to move the entity along
     */
    public EntityInstance move(EntityInstance entity, List<Coordinate> path) throws Exception {
        if (velvetDawn.game.phase != Phase.Game)
            throw new Exception("Invalid game phase to move entities");
    
        if (velvetDawn.game.turns.getActiveTurn() != entity.player.team)
            throw new Exception("You may only move entities on your turn");
    
        // Validate correct path and calculate remaining moves
        var remainingMoves = validateEntityTraversingPath(entity, path);
    
        // Run leave movement triggers
        triggerOnLeaveActions(entity, velvetDawn.map.getTile(entity.position));
    
        // Update the entity to the new position based on the path and the remaining moves
        entity.attributes.set("movement.remaining", Any.from(remainingMoves));
        velvetDawn.entities.setPosition(entity, path.get(path.size() - 1));

        // Run enter movement triggers
        triggerOnEnterActions(entity, velvetDawn.map.getTile(entity.position));
    
        return entity;
    }

    /** Validate an entity's traversal path
     * 
     * This function will raise an exception if the path is invalid.
     * 
     * @param entity The entity to move
     * @param path The path to move the entity
     */
    public int validateEntityTraversingPath(EntityInstance entity, List<Coordinate> path) throws Exception {
        var tiles = path.stream().map(velvetDawn.map::getTile).collect(Collectors.toList());
        var remainingMoves = getRemainingMoves(entity);

        if (!tiles.get(0).position.equals(entity.position))
            throw new Exception("Invalid start position of the entity. The first position in the list, should be where the entity exists.");

        for (int i = 0; i < tiles.size(); i++) {
            var tile = tiles.get(i);

            if (tile == null)
                throw new Exception("null tile found path");

            // Check if the previous tile is a neighbour
            if (i > 0) {
                var prevTile = tiles.get(i - 1);
                if (velvetDawn.map.getNeighbours(tile.position).stream().noneMatch(x -> x.equals(prevTile.position)))
                    throw new Exception("Not all items in the path are neighbours to one-another");
            }

            // If the player already exists in this tile then we don't need to
            // check if it's valid or decrement the remaining moves
            if (tile.position.equals(entity.position))
                continue;

            var tileDefinition = velvetDawn.datapacks.tiles.get(tile.datapackId);
            if (tileDefinition == null)
                throw new Exception(String.format("Unknown tile '%s'", tile.datapackId));

            if (!velvetDawn.map.isTraversable(tile.position))
                throw new Exception("Path traverses through a non-traversable tile");

            if (remainingMoves <= 0)
                throw new Exception("Entity has no remaining moves");

            remainingMoves -= tile.attributes.get(AttributeKeys.TileMovementWeight).toNumber();
        }

        return remainingMoves;
    }
    
    /** Trigger on leave actions
     * 
     * This occurs when an entity leaves a tile, both the tile and unit will be
     * passed here. This function is testing as part of the trigger testing 
     * suite, not movement suite.
     * 
     * @param entity This unit to trigger on
     * @param tile The tile to trigger on
     */
    public void triggerOnLeaveActions(EntityInstance entity, TileInstance tile) throws Exception {
        velvetDawn.datapacks.entities.get(entity.datapackId).triggers.onLeave(entity);
        velvetDawn.datapacks.tiles.get(tile.datapackId).triggers.onLeave(tile);
    }
                
    /** Trigger on enter actions
     * 
     * This occurs when an entity enters a tile, both the tile and unit will be
     * called here.
     * 
     * This function is testing as part of the trigger testing suite, not 
     * movement quite.
     * 
     * @param entity The entity to trigger move actions for
     * @param tileInstance The tile the unit moved to.
     */
    public void triggerOnEnterActions(EntityInstance entity, TileInstance tileInstance) throws Exception {
        velvetDawn.datapacks.entities.get(entity.datapackId).triggers.onEnter(entity);
        velvetDawn.datapacks.tiles.get(tileInstance.datapackId).triggers.onEnter(tileInstance);
    }
}



