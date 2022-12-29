import {get} from "./utils";
import {MapDefinition} from "models/index";

export function getMap(): Promise<MapDefinition> {
    return get("/map/")
}
