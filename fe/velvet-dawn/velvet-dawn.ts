import * as Api from "api"
import {Player} from "models";
import {GamePhrase, GameState} from "models/gameState";
import {LoginDetails} from "models/login-details";
import {TileEntity} from "../renderer/entities/tile-entity";
import {UnitEntity} from "../renderer/entities/unit-entity";
import {Datapacks} from "./datapacks";


export class VelvetDawn {

    public static loginDetails: LoginDetails = {
        username: "error",
        password: "error",
    }

    // Datapack Definitions
    public static datapacks = new Datapacks();
    public static mapWidth = 0
    public static mapHeight = 0

    private static state: GameState = {
        phase: GamePhrase.Lobby,
        turn: -1,
        activeTurn: "-1",
        teams: [],
        players: {},
        setup: {
            commanders: [],
            units: {}
        },
        entities: {},
        spawnArea: []
    }

    // Rendering Entities
    public static map: TileEntity[][] = []
    public static tileEntities: TileEntity[];
    public static unitsDict: { [key: string]: UnitEntity } = {}
    public static spawnAreasSet: boolean = false

    public static audioPlayers: { [key: string]: HTMLAudioElement } = {}

    public static refreshTimer: number = -1

    public static init() {
        clearTimeout(VelvetDawn.refreshTimer)
        // @ts-ignore
        VelvetDawn.refreshTimer = setInterval(() => {
            VelvetDawn.refreshGameState()
        }, 1000);

        return Promise.all([
            VelvetDawn.datapacks.init(),

            Api.map.getMap().then(mapDef => {
                VelvetDawn.mapHeight = mapDef.height
                VelvetDawn.mapWidth = mapDef.width
                VelvetDawn.map = []
                for (let i = 0; i < VelvetDawn.mapWidth; i++) {
                    const col = []
                    for (let j = 0; j < VelvetDawn.mapHeight; j++) {
                        col.push(null);
                    }
                    VelvetDawn.map.push(col)
                }

                VelvetDawn.tileEntities = mapDef.tiles.map((tile) => {
                    let tileEntity = new TileEntity(tile.id, tile.tileId, tile.x, tile.y)
                    VelvetDawn.map[tile.x][tile.y] = tileEntity;
                    return tileEntity
                })
            }),

            VelvetDawn.refreshGameState()
        ])
    }

    static refreshGameState() {
        return Api.game.getState().then(VelvetDawn.setState)
    }

    static getPlayer(): Player {
        if (VelvetDawn.loginDetails && VelvetDawn.state.players[VelvetDawn.loginDetails.username]) {
            return VelvetDawn.state.players[VelvetDawn.loginDetails.username]
        }
        return null
    }

    static getNeighbourTiles(tileX: number, tileY: number): TileEntity[] {
        const isOdd = tileX % 2 === 1

        return [
            {x: tileX - 1, y: isOdd ? tileY : tileY - 1},
            {x: tileX - 1, y: isOdd ? tileY + 1 : tileY},
            {x: tileX, y: tileY - 1},
            {x: tileX, y: tileY},
            {x: tileX, y: tileY + 1},
            {x: tileX + 1, y: isOdd ? tileY : tileY - 1},
            {x: tileX + 1, y: isOdd ? tileY + 1 : tileY}
        ]
            .filter(({ x, y }) => {
                return x >= 0 && y >= 0 && x < VelvetDawn.mapWidth && y < VelvetDawn.mapHeight
            })
            .map(({ x, y }) => {
                return VelvetDawn.map[x][y]
            })
    }

    // static tileClicked(hoveredTile: TileEntity) {
    //     // if (VelvetDawn.state.phase == GamePhrase.Setup) {
    //     //     Api.setup.placeEntity("civil-war:commander", hoveredTile.x, hoveredTile.y)
    //     //         .then((state) => {
    //     //             this.state = state
    //     //         }).catch((x) => {
    //     //             console.log(x)
    //     //         })
    //     // }
    // }

    public static setState(state: GameState) {
        VelvetDawn.state = state

        Object.keys(VelvetDawn.state.entities).forEach(entityId => {
            const serverEntity = VelvetDawn.state.entities[entityId]

            if (VelvetDawn.unitsDict.hasOwnProperty(entityId)) {
                const entity = VelvetDawn.unitsDict[entityId]
                entity.setPosition(serverEntity.position)
            } else {
                VelvetDawn.unitsDict[entityId] = UnitEntity.fromServerInstance(serverEntity);
            }
        });

        Object.keys(VelvetDawn.unitsDict).forEach(entityId => {
            if (!VelvetDawn.state.entities.hasOwnProperty(entityId)) {
                delete VelvetDawn.state.entities[entityId]
            }
        })

        if (VelvetDawn.map.length > 0 && VelvetDawn.state.spawnArea.length > 0 && !VelvetDawn.spawnAreasSet) {
            VelvetDawn.state.spawnArea.forEach(({x, y}) => {
                VelvetDawn.map[x][y].isSpawnArea = true
            })
            VelvetDawn.spawnAreasSet = true
        }
    }

    public static getState() {
        return VelvetDawn.state;
    }
}
