import {Perspective} from "../perspective";
import {RenderingConstants} from "../scenes/scene";

export abstract class Renderable {

    public abstract render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants, timeDelta: number): null;
    
}
