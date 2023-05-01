import * as Api from "api"
import {createBlankState, GamePhase, GameState, LoginDetails, Player} from "models";
import {Datapacks} from "./datapacks";
import {SPECTATORS_TEAM} from "../constants";
import {VelvetDawnMap} from "./map";
import {Renderer} from "../rendering/Renderer";
import {RenderingConstants} from "../rendering/scenes/scene";


export class DebugOptions {

    private lastRenderTime: number = 0
    private lastFrameEnd: number = 0
    private rates: number[] = []
    private pingTime = 0

    public update(frameStart: number, frameEnd: number) {
        this.lastRenderTime = frameEnd - frameStart;

        if (this.lastFrameEnd !== 0) {
            this.rates.push(frameEnd - this.lastFrameEnd)
        }
        this.lastFrameEnd = frameEnd

        if (this.rates.length > 100) {
            this.rates.shift()
        }
    }

    render(ctx: CanvasRenderingContext2D, constants: RenderingConstants) {
        const state = VelvetDawn.getState()
        let total = 0
        this.rates.forEach(x => total += x);
        total /= this.rates.length
        const renderRate = Math.round(total * 100) / 100;

        const framesPerSecond = Math.round(1000 / total * 100) / 100;

        ctx.fillStyle = "#ffffff"
        ctx.textBaseline = "bottom"
        ctx.textAlign = "left"
        ctx.font = "40px arial";
        ctx.fillText(`Render Times: ${this.lastRenderTime} ${renderRate} ${framesPerSecond}`, 10, constants.height - 10)
        ctx.fillText(`Attribute updates: ${state.attributeUpdates.length}`, 10, constants.height - 60)
        ctx.fillText(`Entity updates: ${state.entityUpdates.length + state.entityRemovals.length}`, 10, constants.height - 110)
        ctx.fillText(`Ping: ${this.pingTime}`, 10, constants.height - 160)
    }

    public getLastRenderTime() {
        return this.lastRenderTime
    }

    addPingTime(number: number) {
        this.pingTime = number
    }
}


export class VelvetDawn {

    public static readonly debug = new DebugOptions();

    public static loginDetails: LoginDetails = {
        username: "error",
        password: "error",
    }

    public static datapacks = new Datapacks();
    public static players: { [key: string]: Player } = {}

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
        ]).then(() => {
            Api.game.getState(true).then(VelvetDawn.setState)
        })
    }

    public static initMap() {
        return VelvetDawn.map.init()
    }

    static refreshGameState() {
        let ping = new Date().getTime()
        return Api.game.getState(false).then(state => {
            VelvetDawn.debug.addPingTime(new Date().getTime() - ping)
            VelvetDawn.setState(state)
        })
    }

    static getPlayer(): Player {
        if (VelvetDawn.loginDetails && VelvetDawn.players[VelvetDawn.loginDetails.username]) {
            return VelvetDawn.players[VelvetDawn.loginDetails.username]
        }
        return null
    }

    public static setState(state: GameState) {
        state.players.forEach(player => VelvetDawn.players[player.name] = player);

        VelvetDawn.state = state
        VelvetDawn.map.updateState(state)
        Renderer.getInstance().getScene().onStateUpdate(state)
    }

    public static getState() {
        return VelvetDawn.state;
    }

    static listCurrentTurnPlayers() {
        const state = VelvetDawn.getState()

        if (state.phase === GamePhase.Setup) {
            return Object.keys(VelvetDawn.players).map(x => {
                const player = VelvetDawn.players[x]
                return player.team !== SPECTATORS_TEAM
                 ? player
                 : null
            }).filter(x => x != null)

        } else {
            const turn = state.turn.team

            return Object.keys(VelvetDawn.players).map(x => {
                const player = VelvetDawn.players[x]
                return player.team === turn
                 ? player
                 : null
            }).filter(x => x != null)
        }
    }

    static isPlayersTurn() {
        return VelvetDawn.players[this.loginDetails.username].team === VelvetDawn.state.turn.team
    }
}
