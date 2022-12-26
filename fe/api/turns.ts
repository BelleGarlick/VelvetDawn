import {post} from "api/utils";
import {GameState} from "models";
import { VelvetDawn } from "velvet-dawn/velvet-dawn";


export function ready(): Promise<GameState> {
    return post("/turns/ready/", {
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password
    })
}


export function unready(): Promise<GameState> {
    return post("/turns/unready/", {
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password
    })
}
