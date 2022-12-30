

export interface EntityInstance {
    id: number,
    player: string,
    entity: string,
    position: {
        x: number,
        y: number
    },
    movement: {
        remaining: number
        range: number
    }
}
