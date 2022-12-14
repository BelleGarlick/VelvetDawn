import { Team } from "./team";

export enum GamePhrase {
    Lobby = 'lobby',
    Setup = 'setup',
    Game = 'game',
    GameOver = 'over'
}

export interface GameState {
    phase: GamePhrase,
    turn: number,
    activeTurn: string,
    teams: Team[]
}
