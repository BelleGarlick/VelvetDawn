import {VelvetDawnMap} from "../../../velvet-dawn/map";
import {PathPlanning} from "./path-planning";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";


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
    }
});


const setupMap = async (): Promise<VelvetDawnMap> => {
    const map = new VelvetDawnMap();
    await map.init()

    map.updateState({
        ...VelvetDawn.getState(),
        tileAttrChanges: [
            {instanceId: "1", key: "movement.weight", value: 3},
            {instanceId: "3", key: "movement.weight", value: 3},
            {instanceId: "4", key: "movement.traversable", value: false}
        ]
    })

    return new Promise((resolve) => {
        resolve(map)
    })
}

// Test compute paths
describe("Test compute paths", () => {
    test("Compue paths create cache", async () => {
        const map = await setupMap()

        const pathPlanning = new PathPlanning(map);
        pathPlanning.computePaths({x: 0, y: 0}, 10);

        // Test pointin range
        expect(pathPlanning.isPointInRange({x: 2, y: 2})).toBe(true)
        expect(pathPlanning.isPointInRange({x: 1, y: 1})).toBe(false)  // not traversable

        // Test paths to point
        expect(pathPlanning.getPathToPoint({x: 1, y: 0}).length).toBe(2)
        expect(pathPlanning.getPathToPoint({x: 1, y: 2}).length).toBe(4)
        // This is a little confusing as it's the same length as the previous
        // but it's due to the hexagonal placement
        expect(pathPlanning.getPathToPoint({x: 2, y: 2}).length).toBe(4)
        expect(pathPlanning.getPathToPoint({x: 1, y: 1})).toBeUndefined()  // not traversable

        // Test clear
        pathPlanning.clear()
        expect(pathPlanning.isPointInRange({x: 0, y: 0})).toBeFalsy()
    })
})
