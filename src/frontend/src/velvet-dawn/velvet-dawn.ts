import * as Api from "api"
import {GamePhase, GameState, Player, LoginDetails, createBlankState} from "models";
import {Datapacks} from "./datapacks";
import {SPECTATORS_TEAM} from "../constants";
import {VelvetDawnMap} from "./map";
import {Renderer} from "../rendering/Renderer";

export class VelvetDawn {

    public static loginDetails: LoginDetails = {
        username: "error",
        password: "error",
    }

    public static datapacks = new Datapacks();

    private static firstLoad: boolean = true
    private static state: GameState = createBlankState()

    public static map: VelvetDawnMap;

    public static audioPlayers: { [key: string]: HTMLAudioElement } = {}

    public static refreshTimer: number = -1

    public static init() {
        VelvetDawn.map = new VelvetDawnMap();

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
        if (this.firstLoad) {
            this.firstLoad = false
            return Api.game.getState(true).then(VelvetDawn.setState)
        } else
            return Api.game.getState(false).then(VelvetDawn.setState)
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
