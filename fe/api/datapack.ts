import {get} from "./utils";
import {Tile, Entity, Resource} from "models/index";

export function getDatapacks(): Promise<{
    tiles: Tile[],
    entities: Entity[],
    resources: Resource[]
}> {
    return get("/datapacks/")
}
