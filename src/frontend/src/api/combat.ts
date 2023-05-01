import {post} from "./utils";
import {GameState, Position} from "models";


export function attack(instanceId: string, position: Position): Promise<GameState> {
    return post("combat/attack", {
        instanceId: instanceId,
        x: position.x,
        y: position.y
    })
}
