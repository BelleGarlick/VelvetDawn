import {post} from "./utils";
import {GameState, Position} from "models";
import {VelvetDawn} from "velvet-dawn/velvet-dawn";


export function move(entityPk: number, path: Position[]): Promise<GameState> {
    return post("/move/", {
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password,
        "entity": entityPk,
        "path": JSON.stringify(path)
    })
}
