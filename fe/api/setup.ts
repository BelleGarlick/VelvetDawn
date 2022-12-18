import {post} from "api/utils";
import {GameSetup, GameState} from "models";
import { VelvetDawn } from "velvet-dawn/velvet-dawn";


export function updateGameSetup(entity: string, count: number): Promise<GameSetup> {
    return post("/setup/", {
        entity: entity,
        count: count,
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password
    })
}

export function placeEntity(entity: string, x: number, y: number): Promise<GameState> {
    return post("/setup/add/", {
        entity: entity,
        x: x, y: y,
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password
    })
}

export function removeEntity(x: number, y: number): Promise<GameState> {
    return post("/setup/remove/", {
        x: x, y: y,
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
