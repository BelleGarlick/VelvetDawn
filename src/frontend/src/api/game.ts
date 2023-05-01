import {get} from "./utils";
import {GameState} from "models";


export function getState(firstLoad: boolean): Promise<GameState>  {
    return get(`/game-state/?full-state=${firstLoad}`)
}