import {get} from "api/utils";
import {Entity} from "models/entity";


export function getEntities(): Promise<Entity[]> {
    return get("entities/")
}
