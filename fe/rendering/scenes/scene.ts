import {TileEntity} from "../entities/tile-entity";
import {Perspective} from "../perspective";
import {TurnBanner} from "../entities/turn-banner";
import {Position, GameState} from "models";


export interface RenderingConstants {
    resolution: number

    width: number  // canvas width
    height: number  // canvas width

    sidebar: number  // sidebar width
    sidebarStart: number
    sidebarPadding: number

    buttonSpacing: number
    buttonHeight: number
    buttonWidth: number

    nextTurnButtonStartX: number;
    nextTurnButtonStartY: number;
}


export abstract class Scene {

    protected mousePosition: Position | undefined = undefined

    protected readonly turnBanner = new TurnBanner();

    public hoveredTile: TileEntity | undefined = undefined;
    protected clickedTile: TileEntity | undefined = undefined;

    abstract onStart(constants: RenderingConstants): undefined;
    abstract onStateUpdate(state: GameState): undefined;

    abstract render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): undefined;

    abstract clicked(renderingConstants: RenderingConstants, x: number, y: number): undefined

    public setMousePosition(position: Position | undefined) {
        this.mousePosition = position
    }

    abstract keyboardInput(event: KeyboardEvent): null
}
