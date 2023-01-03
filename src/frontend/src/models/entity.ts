

export interface Entity {
    id: string
    name: string
    commander: boolean,
    textures: {
        background: string
    },
    attributes: {
        icon: string | undefined
        name: string | undefined
        id: string
    }[]
}
