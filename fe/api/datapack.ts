import {get} from "api/utils";
import {Tile} from "models/tile";
import {Entity} from "models/entity";
import {Resource} from "models/resource";

export function getDatapacks(): Promise<{
    tiles: Tile[],
    entities: Entity[],
    resources: Resource[]
}> {
    return get("/datapacks/")
}
