import {post} from "./utils";
import {GameState} from "models";


export function ready(): Promise<GameState> {
    return post("/turns/ready/", {})
}


export function unready(): Promise<GameState> {
    return post("/turns/unready/", {})
}
