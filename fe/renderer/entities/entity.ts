import {Perspective} from "../perspective";

export abstract class Entity {

    public readonly id: string;

    protected constructor(id: string) {
        this.id = id
    }

    public abstract render(ctx: CanvasRenderingContext2D, perspective: Perspective): null;
}
