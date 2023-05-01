import {TileEntity} from "../rendering/entities/tile-entity";
import * as Api from "api";
import {Position, GameState, GamePhase} from "models";
import {VelvetDawn} from "./velvet-dawn";
import {UnitEntity} from "../rendering/entities/unit-entity";


/** This module handles the map state for the game. This includes
 *  - Tracking units and tiles
 *  - Path planning
 *  - Communicating with the server about map changes
 */


export interface PathPlanningNode {
    weight: number
    position: Position
    previous: PathPlanningNode | undefined
}


export class VelvetDawnMap {

    private width: number = 0
    private height: number = 0

    // Tile entities
    private map: TileEntity[][] = []  // Store tile entities in grid
    public tilesById: { [key: string]: TileEntity } = {}
    public tiles: TileEntity[];  // Store the same entity objects but in a list

    // Unit Entities
    private units: { [key: string]: UnitEntity } = {}
    private unitInstanceMap: { [key: string]: UnitEntity } = {}  // Entities stored by hashed coordinate

    /** Initialise the map by loading it from the server
     * and instantiating all the tile entities.
     */
    init() {
        return Api.map.getMap().then(mapDef => {
            this.width = mapDef.width;
            this.height = mapDef.height;

            this.map = []
            for (let i = 0; i < mapDef.width; i++) {
                const col = []
                for (let j = 0; j < mapDef.height; j++) {
                    col.push(null);
                }
                this.map.push(col)
            }

            this.tiles = mapDef.tiles.map((tile) => {
                let tileEntity = new TileEntity(tile.instanceId, tile.tile, tile.position)
                this.tilesById[tile.instanceId] = tileEntity
                this.map[tile.position.x][tile.position.y] = tileEntity;
                return tileEntity
            })

            console.log(this.tiles)
        })
    }

    /** Get a tile at a position */
    getTile({x, y}: Position) {
        return this.map[x][y]
    }

    /** List all units */
    allUnits(): UnitEntity[] { return Object.values(this.units); }

    /** Get the unit based on its instance id */
    getUnit(unitId: string): UnitEntity | undefined {
        return this.units[unitId];
    }

    /** Get a unit at a given position using the hashed coordinate */
    getUnitAtPosition(position: Position): UnitEntity | undefined {
        return this.unitInstanceMap[VelvetDawnMap.hashCoordinate(position)];
    }

    /** Get the neighbours around a tile ordinate
     *
     * @param position: The position to get tiles around
     * @returns The list of neighbouring tile entities
     */
    getNeighbours({x, y}: Position): TileEntity[] {
        const isOdd = x % 2 === 1

        return [
            {x: x - 1, y: isOdd ? y : y - 1},
            {x: x - 1, y: isOdd ? y + 1 : y},
            {x: x, y: y - 1},
            {x: x, y: y + 1},
            {x: x + 1, y: isOdd ? y : y - 1},
            {x: x + 1, y: isOdd ? y + 1 : y}
        ]
            .filter(({ x, y }) => {
                // Check the tile is within the map boundaries
                return x >= 0 && y >= 0 && x < this.width && y < this.height
            })
            .map((position) => {
                return this.getTile(position)
            })
    }

    /** Calculate all possible traversal paths the unit may take.
     *
     * This function will calculate the area around the entity
     * for all paths it may traverse with the given movement points.
     * It will take into account whether a tile is traversable
     * and if there is already and entity there.
     *
     * It works essentially by flood-filling the possible area
     * and using a linked list to store the path
     *
     * @param position
     * @param movementPoints
     */
    getTilesInMovementRange(position: Position, movementPoints: number): PathPlanningNode[] {
        const hashPosition = ({x, y}: Position) => `${x}-${y}`

        // Store list of all checked cells and unchecked cells
        let checkedCoordinates = new Set<string>();
        let uncheckedCoordinates = new Set<string>([hashPosition(position)]);
        let checkedCells: PathPlanningNode[] = [];
        let uncheckedCells: PathPlanningNode[] = [
            {position: position, weight: movementPoints, previous: undefined}
        ]

        // Loop through all cells until there are none left
        while (uncheckedCells.length) {
            // Chose next cell
            let nextCellIndex = -1
            let nextCell: PathPlanningNode | undefined = undefined
            uncheckedCells.forEach((cell, i) => {
                if (!nextCell) {
                    nextCell = cell
                    nextCellIndex = i
                }
                else if (cell.weight > nextCell!.weight) {
                    nextCell = cell
                    nextCellIndex = i
                }
            })

            // Update (un)checked cells
            checkedCells.push(nextCell)
            checkedCoordinates.add(hashPosition(nextCell.position))
            uncheckedCells.splice(nextCellIndex, 1)
            uncheckedCoordinates.delete(hashPosition(nextCell.position))

            // Find next cells
            if (nextCell.weight > 0) {
                const neighbours = this.getNeighbours(nextCell.position)
                neighbours.forEach((tile) => {
                    const tileHash = hashPosition(tile.position)
                    const isTraversable = tile.attributes['movement.traversable'] ?? true
                    const movementWeight = tile.attributes['movement.weight'] ?? 1

                    const isNew = !checkedCoordinates.has(tileHash) && !uncheckedCoordinates.has(tileHash)
                        && this.getUnitAtPosition(tile.position) === undefined

                    if (isNew && isTraversable) {
                        uncheckedCoordinates.add(tileHash)
                        uncheckedCells.push({
                            position: tile.position,
                            weight: nextCell.weight - movementWeight,
                            previous: nextCell
                        })
                    }
                })
            }
        }

        return checkedCells
    }

    /** Move an entity along some path
     *
     * This function will update where it is in the map state
     * to allow instantly accessing the unit and submit the
     * path to the server to then update the entities position.
     *
     * @param entityId The id of the entity to update
     * @param path The path the entity traverses.
     */
    move(entityId: string, path: Position[]) {
        if (path.length < 1)
            return

        const unit = this.units[entityId];
        const newPosition = path[path.length - 1]

        delete this.unitInstanceMap[VelvetDawnMap.hashCoordinate(unit.getPosition())]
        unit.setPosition(newPosition)
        this.unitInstanceMap[VelvetDawnMap.hashCoordinate(newPosition)] = unit;

        Api.units.move(entityId, path)
            .then(x => VelvetDawn.setState(x))
            .catch(x => {
                // TODO pop up message showing why reason is wrong
                // Dont need to move entity back, just wait until the game state refreshes
                console.log("Move entity back")
            })
    }

    /** Called when the game state is reloaded every second.
     *
     * This function handles updating, creating
     * and removing all entities
     *
     * @param state The latest state of the game given by the server.
     */
    updateState(state: GameState) {
        // Update / create updates entities
        state.entityUpdates.forEach(entity => {
            let currentInstance = this.units[entity.instanceId];

            // Remove current instant from current position
            if (currentInstance) {
                const key = VelvetDawnMap.hashCoordinate(currentInstance.getPosition())
                delete this.unitInstanceMap[key]
            }
            else {
                currentInstance = new UnitEntity(entity.instanceId, entity.unit, entity.player);
            }
            currentInstance.setPosition(entity.position)

            // Update the entity and entity map position
            this.units[entity.instanceId] = currentInstance
            this.unitInstanceMap[VelvetDawnMap.hashCoordinate(entity.position)] = currentInstance;
        });

        // Clear up old units if they've been removed
        state.entityRemovals.forEach(instanceId => {
            let unit = this.units[instanceId];
            delete this.unitInstanceMap[VelvetDawnMap.hashCoordinate(unit.position)]
            delete this.units[instanceId]
        })

        state.attributeUpdates.forEach((attrUpdate) => {
            if (attrUpdate.type === "tile") {
                let instance = this.tilesById[attrUpdate.instanceId];
                if (instance == null) {

                } else {
                    // console.log("---")
                    // console.log(this.tilesById[attrUpdate.instanceId].attributes[attrUpdate.attribute])
                    // console.log(attrUpdate.instanceId)
                    // console.log(attrUpdate.attribute)
                    // console.log(attrUpdate.value)

                    this.tilesById[attrUpdate.instanceId].attributes[attrUpdate.attribute] = attrUpdate.value
                }


            } else if (attrUpdate.type === "entity")
                this.units[attrUpdate.instanceId].attributes[attrUpdate.attribute] = attrUpdate.value
            else
                console.error("Unknown attribute upgrade " + attrUpdate.type)
        });
    }

    /** Used to store positions in the dict, this will
     * has the position turning it into a string
     *
     * @param position The position to hash
     * @private the hashed position
     */
    private static hashCoordinate(position: Position): string {
        return `${position.x}-${position.y}`
    }

    /** Used only in the setup state, this will remove an entity from the map
     * If there is an error however the state update will just re-create that
     * entity
     *
     * @param position: The position to remove the entity from.
     */
    removeEntityDuringSetup(position: Position) {
        if (VelvetDawn.getState().phase === GamePhase.Setup) {
            const selectedEntity = this.getUnitAtPosition(position)
            if (selectedEntity) {
                delete this.units[selectedEntity.instanceId]
                delete this.unitInstanceMap[VelvetDawnMap.hashCoordinate(selectedEntity.getPosition())]
            }

            Api.setup.removeEntity(position)
                .then(x => {
                    VelvetDawn.setState(x)
                })
                .catch(x => {
                    // Dont need to move entity back, just wait until the game state refreshes
                    // TODO Popup
                    console.info(x)
                })
        }
    }

    /** Get the distance between two hex-positions
     *
     * @param origin Position a
     * @param to Position b
     * @returns The distance between the tiles
     */
    getDistance(origin: Position, to: Position) {
        const dcol = Math.abs(origin.x - to.x)
        const drow = Math.abs(origin.y - to.y)

        const distance = Math.max(dcol, drow + dcol / 2)

        if (origin.x % 2 === 0 && dcol % 2 === 1) {
            if (to.y <= origin.y)
                return Math.floor(distance)
            return Math.ceil(distance)
        }
        else if (dcol % 2 === 1) {
            if (to.y <= origin.y)
                return Math.ceil(distance)
            return Math.floor(distance)
        }

        return Math.round(distance)
    }

    /** List all units in range
     *
     * @param position Position units must be in range of
     * @param range Max distance between the unit and given position
     * @returns Units in range
     */
    getUnitsInRange(position: Position, range: number) {
        const inRangeUnits: UnitEntity[] = []

        Object.values(this.units).forEach(unit => {
            if (this.getDistance(position, unit.getPosition()) <= range) {
                inRangeUnits.push(unit)
            }
        });

        return inRangeUnits;
    }
}
