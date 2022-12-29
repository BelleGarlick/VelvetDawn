import { EntityInstance } from "./entity-instance";


export interface Player {
    name: string,
    spectating: boolean,
    admin: boolean,
    entities: EntityInstance[],
    team: string,
    ready: boolean
}
