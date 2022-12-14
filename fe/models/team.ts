import {Player} from "models/player";


export interface Team {
    name: string,
    color: string,
    players: Player[]
}
