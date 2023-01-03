import {TileEntity} from "../entities/tile-entity";
import {TurnBanner} from "../entities/turn-banner";
import {GameState} from "models";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {RenderingFacade} from "../facade";


export interface RenderingConstants {
    tabHeight: number;
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

    protected readonly turnBanner = new TurnBanner();

    public hoveredTile: TileEntity | undefined = undefined;
    protected clickedTile: TileEntity | undefined = undefined;

    abstract onStart(facade: RenderingFacade): undefined;
    abstract onStateUpdate(state: GameState): undefined;

    abstract render(facade: RenderingFacade): undefined;

    abstract clicked(renderingConstants: RenderingConstants, x: number, y: number): undefined

    abstract keyboardInput(event: KeyboardEvent): null

    protected renderTiles(facade: RenderingFacade) {
        VelvetDawn.map.tiles.forEach(tile => tile.render(facade))
    }

    protected renderUnits(facade: RenderingFacade) {
        // TODO Entity culling and updating if pos is outside window + 1 border for animating
        VelvetDawn.map.allUnits().forEach(unit => {
            unit.render(facade)
        })
    }
}
