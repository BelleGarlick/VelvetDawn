import {Perspective} from "../perspective";
import {RenderingConstants} from "../phases/scene";

export abstract class Renderable {

    public abstract render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): null;
    
}
