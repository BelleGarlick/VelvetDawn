import * as Api from "api"
import {Entity, Tile, Resource, ResourceType} from "models";
import {getUrl} from "api/utils";
import {MENU_AUDIO_ID} from "../constants";
import {GamePhrase, GameState} from "models/gameState";
import {Team} from "models/team";
import {LoginDetails} from "models/login-details";


export class VelvetDawn {

    public static loginDetails: LoginDetails = {
        username: "error",
        password: "error",
    }

    public static entities: { [key: string]: Entity } = {}
    public static tiles: { [key: string]: Tile } = {}
    public static resources: { [key: string]: Resource } = {}

    public static state: GameState = {
        phase: GamePhrase.Lobby,
        turn: -1,
        activeTurn: "-1",
        teams: []
    }

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
                resources.forEach(resource => {
                    VelvetDawn.resources[resource.id] = resource
                    if (resource.type == ResourceType.Audio && resource.id !== MENU_AUDIO_ID)  // Menu audio is loaded before here so it auto plays
                        VelvetDawn.audioPlayers[resource.id] = new Audio(`${getUrl()}resources/velvet-dawn:menu.mp3/`)
                    if (resource.type == ResourceType.Image)
                        console.info("TODO Load images soon")
                })
            }),
            this.refreshGameState()
        ])
    }

    static refreshGameState() {
        return Api.game.getState()
            .then(x => this.state = x)
            .finally(() => console.log(this.state))
    }
}
