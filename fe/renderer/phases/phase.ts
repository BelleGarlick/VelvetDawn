import {TileEntity} from "../entities/tile-entity";


export interface RenderingConstants {
    width: number  // canvas width
    height: number  // canvas width
    sidebar: number  // sidebar width
}


export abstract class PhaseScene {

    public hoveredTile: TileEntity | undefined = undefined;
    protected clickedTile: TileEntity | undefined = undefined;

    abstract renderSidebar(ctx: CanvasRenderingContext2D, constants: RenderingConstants): undefined;
}
