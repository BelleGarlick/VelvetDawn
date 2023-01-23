
export interface TileInstance {
    instanceId: string

    tile: string

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
