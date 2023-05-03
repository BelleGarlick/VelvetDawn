import {Position} from "models/position";


export class PositionSet {

    private positions: Set<string> = new Set<string>();


    private hash(position: Position): string {
        return `${position.x}-${position.y}`
    }

    public add(position: Position) {
        this.positions.add(this.hash(position))
        return this;
    }

    public addAll(positions: Position[]) {
        positions.forEach(position => this.positions.add(this.hash(position)));
        return this;
    }

    public has(position: Position) {
        return this.positions.has(this.hash(position))
    }

    public items(): Position[] {
        var items: Position[] = []
        this.positions.forEach((x: string) => {
            var tokens = x.split("-");
            items.push({x: parseFloat(tokens[0]), y: parseFloat(tokens[1])})
        })
        return items;
    }

    clear() {
        this.positions.clear();
    }
}
