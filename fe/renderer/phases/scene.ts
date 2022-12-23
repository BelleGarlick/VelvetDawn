import {TileEntity} from "../entities/tile-entity";
import {Perspective} from "../perspective";


export interface RenderingConstants {
    width: number  // canvas width
    height: number  // canvas width
    sidebar: number  // sidebar width
    sidebarPadding: number
}


export abstract class Scene {

    public hoveredTile: TileEntity | undefined = undefined;
    protected clickedTile: TileEntity | undefined = undefined;

    abstract onStart(constants: RenderingConstants): undefined;

    abstract renderSidebar(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): undefined;

    abstract clicked(renderingConstants: RenderingConstants, x: number, y: number): undefined
}
