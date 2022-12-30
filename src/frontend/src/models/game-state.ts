import { Team } from "./team";
import {Player, EntityInstance} from "models/index";

export enum GamePhrase {
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
    team: string | undefined  // current team who's turn it is
    number: number  // The turn number
    start: number  // The unix epoch time the turn started
    seconds: number  // The current length of the turn in seconds
}

export interface GameState {
    phase: GamePhrase,
    turn: TurnData,
    teams: Team[],
    players: { [key: string]: Player },
    setup: GameSetup,
    entities: { [key: string]: EntityInstance },
    spawnArea: {
        x: number,
        y: number
    }[]
}
