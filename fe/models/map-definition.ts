
export interface TileInstance {
    x: number
    y: number
    id: string
}


export interface MapDefinition {
    width: number
    height: number
    tiles: TileInstance[]
}
