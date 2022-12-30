import * as Api from "api"
import {GamePhrase, GameState, Player, LoginDetails} from "models";
import {Datapacks} from "./datapacks";
import {SPECTATORS_TEAM} from "../constants";
import {VelvetDawnMap} from "./map";
import {Renderer} from "../rendering/Renderer";

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
        turn: {
            team: null,
            number: -1,
            start: -1,
            seconds: -1
        },
        teams: [],
        players: {},
        setup: {
            commanders: [],
            units: {},
            placedCommander: false,
            remainingUnits: {}
        },
        entities: {},
        spawnArea: []
    }

    public static map: VelvetDawnMap = new VelvetDawnMap();

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
            VelvetDawn.map.init(),
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

    public static setState(state: GameState) {
        VelvetDawn.state = state
        VelvetDawn.map.updateState(state)
        Renderer.getInstance().getScene().onStateUpdate(state)
    }

    public static getState() {
        return VelvetDawn.state;
    }

    static listCurrentTurnPlayers() {
        const state = VelvetDawn.getState()
        if (state.phase === 'setup') {
            return Object.keys(state.players).map(x => {
                const player = state.players[x]
                return player.team !== SPECTATORS_TEAM
                 ? player
                 : null
            }).filter(x => x != null)
        } else {
            const turn = state.turn.team

            return Object.keys(state.players).map(x => {
                const player = state.players[x]
                return player.team === turn
                 ? player
                 : null
            }).filter(x => x != null)
        }
    }

    static isPlayersTurn() {
        return VelvetDawn.state.players[this.loginDetails.username].team === VelvetDawn.state.turn.team
    }
}
