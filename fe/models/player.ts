import { EntityInstance } from "./entityInstance";


export interface Player {
    name: string,
    spectating: boolean,
    entities: EntityInstance[]
}
