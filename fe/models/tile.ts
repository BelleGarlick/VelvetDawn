

export interface Tile {
    id: string,
    name: string,
    movement: {
        penalty: number,
        traversable: boolean
    }
}
