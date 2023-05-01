import {post} from "./utils";
import {GameSetup, GameState, Position} from "models";


export function updateGameSetup(entity: string, count: number): Promise<GameSetup> {
    return post("/setup/", {
        entity: entity,
        count: count
    })
}

export function placeEntity(entity: string, position: Position): Promise<GameState> {
    return post("/setup/add/", {
        entity: entity,
        x: position.x,
        y: position.y
    })
}

export function removeEntity(position: Position): Promise<GameState> {
    return post("/setup/remove/", {
        x: position.x,
        y: position.y
    })
}


export function startSetup(): Promise<GameState> {
    return post("/setup/start-setup/", {})
}
