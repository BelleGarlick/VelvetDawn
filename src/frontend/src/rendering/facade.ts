import {Perspective} from "./perspective";
import {RenderingConstants} from "./scenes/scene";
import {Position} from "models/position";


const RESOLUTION = 2;


export class RenderingFacade {

    ctx: CanvasRenderingContext2D;
    perspective: Perspective;
    constants: RenderingConstants;
    timeDelta: number;
    mousePosition: undefined | Position

    /** Constants */
    public resolution = RESOLUTION
    public width = 0
    public height = 0;

    public sidebarStart = 0
    public sidebarWidth = 300 * RESOLUTION
    public sidebarPadding = 10 * RESOLUTION
    public sidebarInnerStart = 0

    public recalculateConstants() {
        this.constants = this.getConstants()

        this.width = window.innerWidth * RESOLUTION
        this.height = window.innerHeight * RESOLUTION

        this.sidebarStart = this.width - this.sidebarWidth
        this.sidebarInnerStart = this.sidebarStart + this.sidebarPadding

        return this
    }

    getConstants(): RenderingConstants {
        const width = window.innerWidth * RESOLUTION
        const sidebarWidth = 300 * RESOLUTION
        const sidebarPadding = 10 * RESOLUTION
        const sidebarStart = width - sidebarWidth
        const height = window.innerHeight * RESOLUTION

        const buttonHeight = 50 * RESOLUTION

        return {
            resolution: RESOLUTION,

            tabHeight: 35 * RESOLUTION,

            width: width,
            height: height,
            sidebar: sidebarWidth,
            sidebarPadding: sidebarPadding,
            sidebarStart: sidebarStart,

            buttonSpacing: 10 * RESOLUTION,
            buttonHeight: buttonHeight,
            buttonWidth: sidebarWidth - sidebarPadding - sidebarPadding,
            nextTurnButtonStartX: sidebarStart + sidebarPadding,
            nextTurnButtonStartY: height - buttonHeight - sidebarPadding
        }
    }
}
