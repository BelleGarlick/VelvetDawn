import {post} from "./utils";
import {GameSetup, GameState, Position} from "models/index";
import { VelvetDawn } from "velvet-dawn/velvet-dawn";


export function updateGameSetup(entity: string, count: number): Promise<GameSetup> {
    return post("/setup/", {
        entity: entity,
        count: count,
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password
    })
}

export function placeEntity(entity: string, position: Position): Promise<GameState> {
    return post("/setup/add/", {
        entity: entity,
        x: position.x, y: position.y,
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password
    })
}

export function removeEntity(position: Position): Promise<GameState> {
    return post("/setup/remove/", {
        x: position.x, y: position.y,
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password
    })
}


export function startSetup(): Promise<GameState> {
    return post("/setup/start-setup/", {
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password
    })
}
