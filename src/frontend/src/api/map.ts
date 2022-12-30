import {get} from "./utils";
import {MapDefinition} from "models";

export function getMap(): Promise<MapDefinition> {
    return get("/map/")
}
