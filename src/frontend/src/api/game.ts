import {get} from "./utils";
import {GameState} from "models";
import {VelvetDawn} from "../velvet-dawn/velvet-dawn";


export function getState(firstLoad: boolean): Promise<GameState>  {
    return get(`/game-state/?username=${VelvetDawn.loginDetails.username}&password=${VelvetDawn.loginDetails.password}&full-state=${firstLoad}`)
}