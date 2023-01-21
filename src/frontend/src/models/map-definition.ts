
export interface TileInstance {
    id: string

    tileId: string

    position: {
        x: number
        y: number
    }
}


export interface MapDefinition {
    width: number
    height: number
    tiles: TileInstance[]
}
