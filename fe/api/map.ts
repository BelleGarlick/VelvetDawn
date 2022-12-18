import {get} from "api/utils";
import {Tile} from "models/tile";
import {MapDefinition} from "models/map-definition";


export function getTiles(): Promise<Tile[]> {
    return get("/map/tiles/")
}


export function getMap(): Promise<MapDefinition> {
    return get("/map/")
}
