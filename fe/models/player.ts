import { EntityInstance } from "./entityInstance";


export interface Player {
    name: string,
    spectating: boolean,
    admin: boolean,
    entities: EntityInstance[],
    team: string,
    ready: boolean
}
