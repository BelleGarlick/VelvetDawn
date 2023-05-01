import {post} from "./utils";
import {GameState, Position} from "models";


export function attack(instanceId: string, position: Position): Promise<GameState> {
    return post("combat/attack", {
        attackerId: instanceId,
        targetX: position.x,
        targetY: position.y
    })
}
