import {get} from "./utils";
import {Tile, EntityDefinition, Resource} from "models";

export function getDatapacks(): Promise<{
    tiles: Tile[],
    entities: EntityDefinition[],
    resources: Resource[]
}> {
    return get("/datapacks/")
}
