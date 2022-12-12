import {get} from "api/utils";
import {Tile} from "models/tile";


export function getTiles(): Promise<Tile[]> {
    return get("map/tiles/")
}
