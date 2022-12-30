

export interface Tile {
    id: string,
    name: string,
    movement: {
        weight: number,
        traversable: boolean
    }
}
