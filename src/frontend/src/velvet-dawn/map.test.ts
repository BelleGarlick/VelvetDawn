import {VelvetDawnMap} from "./map";
import {VelvetDawn} from "./velvet-dawn";
import {createBlankState, GamePhase} from "models/game-state";

/** Test the VelvetDawn map class' various functions */

const mockBlankState = createBlankState()

jest.mock('api', () => {
    return {
        map: {
            getMap: () => {
                return new Promise((resolve) => {
                    resolve({
                        width: 3,
                        height: 3,
                        tiles: [
                            {id: 0, tileId: "test:grass", x: 0, y: 0, color: '#000000'},
                            {id: 1, tileId: "test:void", x: 0, y: 1, color: '#000000'},
                            {id: 2, tileId: "test:grass", x: 0, y: 2, color: '#000000'},
                            {id: 3, tileId: "test:void", x: 1, y: 0, color: '#000000'},
                            {id: 4, tileId: "test:wall", x: 1, y: 1, color: '#000000'},
                            {id: 5, tileId: "test:grass", x: 1, y: 2, color: '#000000'},
                            {id: 6, tileId: "test:grass", x: 2, y: 0, color: '#000000'},
                            {id: 7, tileId: "test:grass", x: 2, y: 1, color: '#000000'},
                            {id: 8, tileId: "test:grass", x: 2, y: 2, color: '#000000'},
                        ]
                    })
                });
            }
        },
        units: {
            move: () => {
                return new Promise((resolve) => {
                    resolve(mockBlankState)
                })
            }
        },
        setup: {
            removeEntity: () => {
                return new Promise((resolve) => {
                    resolve(mockBlankState)
                })
            }
        }
    }
});

const blankEntity = {
    player: "player",
    entity: "commander",
    movement: {
        remaining: 3,
        range: 4
    }
}

const setupMap = async (setupEntity: boolean): Promise<VelvetDawnMap> => {
    const map = new VelvetDawnMap();
    await map.init()

    if (setupEntity)
        map.updateState({
            ...VelvetDawn.getState(),
            entities: {
                0: {...blankEntity, id: 0, position: {x: 0, y: 0}}
            }
        })

    VelvetDawn.datapacks.tiles = {
        "test:grass": {
            id: "tile:grass",
            name: "Grass",
            movement: { weight: 1, traversable: true }
        },
        "test:void": {
            id: "test:void",
            name: "Void",
            movement: { weight: 3, traversable: true }
        },
        "test:wall": {
            id: "test:wall",
            name: "Wall",
            movement: { weight: 1, traversable: false }
        }
    }

    return new Promise((resolve) => {
        resolve(map)
    })
}


describe("Test init", () => {
    test("Init loads map properly", async () => {
        const map = await setupMap(true);
        const tile = map.getTile({x: 0, y: 0})

        expect(tile.instanceId).toBe(0)
        expect(tile.entityId).toBe("test:grass")
        expect(map.tiles.length).toBe(9)
    })
})

describe("Test get neighbours", () => {
    test("neighbours in center", async () => {
        const map = await setupMap(true);

        const neighbours = map.getNeighbours({x: 1, y: 1})
        expect(neighbours.length).toBe(6)
    })

    test("neighbours at edge", async () => {
        const map = new VelvetDawnMap();
        await map.init()

        const neighbours = map.getNeighbours({x: 2, y: 1})
        expect(neighbours.length).toBe(4)
    })

    test("neighbours in corner", async () => {
        const map = new VelvetDawnMap();
        await map.init()

        const neighbours = map.getNeighbours({x: 2, y: 2})
        expect(neighbours.length).toBe(3)
    })
})

describe("Test update from state", () => {
    test("the state updates correctly with new requests", async () => {
        const map = await setupMap(true);

        const unit = map.getUnit('0')
        expect(map.allUnits().length).toBe(1)
        expect(unit.instanceId).toBe(0)
        expect(map.getUnitAtPosition({x: 0, y: 0}).instanceId).toBe(0)

        map.updateState({
            ...VelvetDawn.getState(),
            entities: {
                0: {...blankEntity, id: 0, position: {x: 1, y: 0}}
            }
        })
        expect(map.allUnits().length).toBe(1)
        expect(unit.getPosition().x).toBe(1)

        map.updateState({
            ...VelvetDawn.getState(),
            entities: {
                0: {...blankEntity, id: 0, position: {x: 1, y: 0}},
                1: {...blankEntity, id: 1, position: {x: 0, y: 0}}
            }
        })

        expect(map.allUnits().length).toBe(2)
        expect(map.getUnitAtPosition({x: 1, y: 0}).instanceId).toBe(0)
        expect(map.getUnitAtPosition({x: 0, y: 0}).instanceId).toBe(1)

        map.updateState({
            ...VelvetDawn.getState(),
            entities: {
                1: {...blankEntity, id: 1, position: {x: 0, y: 0}}
            }
        })

        expect(map.getUnitAtPosition({x: 0, y: 0}).instanceId).toBe(1)
        expect(map.getUnitAtPosition({x: 1, y: 0})).toBeUndefined()
        expect(map.allUnits().length).toBe(1)
    })
})

describe("Test move entity", () => {
    test("the state updates correctly with new requests", async () => {
        const map = await setupMap(true);

        const unit = map.getUnit('0')
        expect(map.allUnits().length).toBe(1)
        expect(unit.instanceId).toBe(0)
        expect(map.getUnitAtPosition({x: 0, y: 0}).instanceId).toBe(0)

        map.move(0, [{x: 0, y: 0}, {x: 1, y: 1}, {x: 2, y: 2}])
        expect(map.getUnitAtPosition({x: 2, y: 2}).instanceId).toBe(0)
        expect(unit.getPosition()).toStrictEqual({x: 2, y: 2})
    })
})

describe("Test remove entity in setup", () => {
    test("the state updates correctly with new requests", async () => {
        VelvetDawn.getState().phase = GamePhase.Lobby
        const map = await setupMap(true);

        const unit = map.getUnit('0')
        expect(map.allUnits().length).toBe(1)
        expect(unit.instanceId).toBe(0)
        expect(map.getUnitAtPosition({x: 0, y: 0}).instanceId).toBe(0)

        // Didn't remove as not in setup
        map.removeEntityDuringSetup({x: 0, y: 0})
        expect(map.allUnits().length).toBe(1)

        VelvetDawn.getState().phase = GamePhase.Setup
        map.removeEntityDuringSetup({x: 0, y: 0})
        expect(map.allUnits().length).toBe(0)
    })
})

describe("Test entities in movement range", () => {
    test("All paths bar non traversable", async () => {
        const map = await setupMap(true);

        // Should be able to move everywhere
        const paths = map.getTilesInMovementRange({x: 0, y: 0}, 10)
        expect(paths.length).toBe(8)  // would be 9 but one tile is not traversable
    })

    test("Path blocked", async () => {
        const map = await setupMap(false);

        // Spawn entities surrounding the current so there are no paths
        map.updateState({
            ...VelvetDawn.getState(),
            entities: {
                0: {...blankEntity, id: 0, position: {x: 0, y: 0}},
                1: {...blankEntity, id: 1, position: {x: 1, y: 0}},
                2: {...blankEntity, id: 2, position: {x: 0, y: 1}}
            }
        })

        const paths = map.getTilesInMovementRange({x: 0, y: 0}, 10)
        expect(paths.length).toBe(1)
    })

    test("Smaller range", async () => {
        const map = await setupMap(true);

        // Small range can only move into surrounding tiles
        const paths = map.getTilesInMovementRange({x: 0, y: 0}, 1)
        expect(paths.length).toBe(3)
    })

    test("High penalty tile", async () => {
        const map = await setupMap(true);

        const paths = map.getTilesInMovementRange({x: 0, y: 0}, 3)
        expect(paths.length).toBe(3)
    })
})