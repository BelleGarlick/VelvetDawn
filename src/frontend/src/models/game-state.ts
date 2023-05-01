import { Team } from "./team";
import {Player, UnitUpdate} from "models/index";
import {Attribute} from "models/attribute";

export enum GamePhase {
    Lobby = 'Lobby',
    Setup = 'Setup',
    Game = 'Game',
    GameOver = 'Over'
}

export interface GameSetup {
    commanders: string[]
    entities: { [key: string]: number }
    placedCommander: boolean
    remainingEntities: { [key: string]: number }
}

export interface TurnData {
    team: string | undefined  // current team whos turn it is
    start: number | undefined  // The unix epoch time the turn started
    seconds: number | undefined  // The current length of the turn in seconds
}

export interface GameState {
    phase: GamePhase,
    turn: TurnData,
    teams: Team[],
    players: Player[],
    setup: GameSetup,
    entityUpdates: UnitUpdate[],
    entityRemovals: string[],
    //
    //     updates: UnitUpdate[],
    //     removed: UnitUpdate[],
    // },
    spawnArea: {
        x: number,
        y: number
    }[],
    attributeUpdates: Attribute[]
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
        players: [],
        setup: {
            commanders: [],
            entities: {},
            placedCommander: false,
            remainingEntities: {}
        },
        entityUpdates: [],
        entityRemovals: [],
        spawnArea: [],
        attributeUpdates: []
    }
}