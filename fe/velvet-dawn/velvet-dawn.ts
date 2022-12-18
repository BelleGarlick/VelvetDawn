import * as Api from "api"
import {Entity, Tile, Resource, ResourceType, Player} from "models";
import {getUrl} from "api/utils";
import {MENU_AUDIO_ID} from "../constants";
import {GamePhrase, GameState} from "models/gameState";
import {LoginDetails} from "models/login-details";
import {Textures} from "../renderer/Textures";
import {TileEntity} from "../renderer/entities/tile-entity";
import {UnitEntity} from "../renderer/entities/unit-entity";


export class VelvetDawn {

    public static loginDetails: LoginDetails = {
        username: "error",
        password: "error",
    }

    // Datapack Definitions
    public static entities: { [key: string]: Entity } = {}
    public static tiles: { [key: string]: Tile } = {}
    public static resources: { [key: string]: Resource } = {}
    public static mapWidth = 0
    public static mapHeight = 0

    public static state: GameState = {
        phase: GamePhrase.Lobby,
        turn: -1,
        activeTurn: "-1",
        teams: [],
        players: {},
        setup: {
            commanders: [],
            units: {}
        }
    }

    // Rendering Entities
    public static map: TileEntity[][] = []
    public static tileEntities: TileEntity[];
    public static unitEntities: UnitEntity[];

    public static audioPlayers: { [key: string]: HTMLAudioElement } = {}

    public static refreshTimer: number = -1

    public static init() {
        clearTimeout(this.refreshTimer)
        // @ts-ignore
        this.refreshTimer = setInterval(() => {
            this.refreshGameState()
        }, 1000);

        return Promise.all([
            Api.entities.getEntities().then(entities => {
                entities.forEach(entity => VelvetDawn.entities[entity.id] = entity)
            }),

            Api.map.getTiles().then(tiles => {
                tiles.forEach(tile => VelvetDawn.tiles[tile.id] = tile)
            }),

            Api.resources.getResources().then(resources => {
                const imageIds: string[] = []
                resources.forEach(resource => {
                    VelvetDawn.resources[resource.id] = resource
                    if (resource.type == ResourceType.Audio && resource.id !== MENU_AUDIO_ID)  // Menu audio is loaded before here so it auto plays
                        VelvetDawn.audioPlayers[resource.id] = new Audio(`${getUrl()}/resources/velvet-dawn:menu.mp3/`)
                    if (resource.type == ResourceType.Image)
                        imageIds.push(resource.id)
                })
                Textures.load(imageIds)
            }),

            Api.map.getMap().then(mapDef => {
                this.mapHeight = mapDef.height
                this.mapWidth = mapDef.width
                this.map = []
                for (let i = 0; i < this.mapWidth; i++) {
                    const col = []
                    for (let j = 0; j < this.mapHeight; j++) {
                        col.push(null);
                    }
                    this.map.push(col)
                }

                this.tileEntities = mapDef.tiles.map((tile) => {
                    let tileEntity = new TileEntity(tile.id, tile.x, tile.y)
                    this.map[tile.x][tile.y] = tileEntity;
                    return tileEntity
                })
            }),

            this.refreshGameState()
        ])
    }

    static refreshGameState() {
        return Api.game.getState()
            .then(x => this.state = x)
    }

    static getPlayer(): Player {
        if (VelvetDawn.loginDetails && VelvetDawn.state.players[VelvetDawn.loginDetails.username]) {
            return VelvetDawn.state.players[VelvetDawn.loginDetails.username]
        }
        return null
    }

    static getNeighbourTiles(tileX: number, tileY: number): TileEntity[] {
        const isOdd = tileX % 2 == 1

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
                return this.map[x][y]
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
}
