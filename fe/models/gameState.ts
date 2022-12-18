import { Team } from "./team";
import {Player} from "models";

export enum GamePhrase {
    Lobby = 'lobby',
    Setup = 'setup',
    Game = 'game',
    GameOver = 'over'
}


export interface GameSetup {
    commanders: string[]
    units: { [key: string]: number },
}


export interface GameState {
    phase: GamePhrase,
    turn: number,
    activeTurn: string,
    teams: Team[],
    players: { [key: string]: Player },
    setup: GameSetup
}
