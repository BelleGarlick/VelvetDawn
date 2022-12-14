import {get} from "api/utils";


export function getState() {
    return get("game-state/")
}