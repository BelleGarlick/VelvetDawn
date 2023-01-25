import {post} from "./utils";
import {GameState, Position} from "models";
import {VelvetDawn} from "../velvet-dawn/velvet-dawn";


export function attack(instanceId: string, position: Position): Promise<GameState> {
    return post("combat/attack", {
        username: VelvetDawn.loginDetails.username,
        password: VelvetDawn.loginDetails.password,
        attackerId: instanceId,
        targetX: position.x,
        targetY: position.y
    })
}
