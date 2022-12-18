import {get} from "api/utils";
import {Resource} from "models/resource";


export function getResources(): Promise<Resource[]> {
    return get("/resources/")
}
