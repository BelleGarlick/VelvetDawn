import {get} from "api/utils";
import {GameState} from "models/gameState";


export function getState(): Promise<GameState>  {
    return get("/game-state/")
}