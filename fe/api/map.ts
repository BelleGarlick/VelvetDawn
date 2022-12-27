import {get} from "api/utils";
import {MapDefinition} from "models/map-definition";

export function getMap(): Promise<MapDefinition> {
    return get("/map/")
}
