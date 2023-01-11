

export interface EntityInstance {
    id: number,
    player: string,
    entity: string,
    position: {
        x: number,
        y: number
    }
}

export type UnitInstance = EntityInstance;
