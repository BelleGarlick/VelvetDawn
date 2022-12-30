

export interface Entity {
    id: string
    name: string
    commander: boolean,
    textures: {
        background: string
    },
    movement: {
        range: number
    }
}
