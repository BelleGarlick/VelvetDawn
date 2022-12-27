
export interface TileInstance {
    id: number

    tileId: string

    x: number
    y: number,

    color: string
    texture: string | undefined
}


export interface MapDefinition {
    width: number
    height: number
    tiles: TileInstance[]
}
