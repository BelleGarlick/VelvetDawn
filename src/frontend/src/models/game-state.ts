import { Team } from "./team";
import {Player, UnitUpdate} from "models/index";
import {Attribute} from "models/attribute";

export enum GamePhase {
    Lobby = 'lobby',
    Setup = 'setup',
    Game = 'game',
    GameOver = 'over'
}

export interface GameSetup {
    commanders: string[]
    units: { [key: string]: number }
    placedCommander: boolean
    remainingUnits: { [key: string]: number }
}

export interface TurnData {
    team: string | undefined  // current team whos turn it is
    start: number  // The unix epoch time the turn started
    seconds: number  // The current length of the turn in seconds
}

export interface GameState {
    phase: GamePhase,
    turn: TurnData,
    teams: Team[],
    players: { [key: string]: Player },
    setup: GameSetup,
    unitChanges: {
        updates: UnitUpdate[],
        removed: UnitUpdate[],
    },
    spawnArea: {
        x: number,
        y: number
    }[],
    attrChanges: Attribute[]
}


export const createBlankState = (): GameState => {
    return {
        phase: GamePhase.Lobby,
        turn: {
            team: null,
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
        unitChanges: {
            updates: [],
            removed: [],
        },
        spawnArea: [],
        attrChanges: []
    }
}