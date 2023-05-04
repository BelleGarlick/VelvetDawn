import {Perspective} from "./perspective";
import {RenderingConstants} from "./scenes/scene";
import {Position} from "models/position";


const RESOLUTION = 2;


export interface RenderHexagonOptions {
    color?: string
    stroke?: string
    strokeWidth?: number
    opacity?: number
}


export class RenderingFacade {

    ctx: CanvasRenderingContext2D;
    perspective: Perspective;
    constants: RenderingConstants;
    timeDelta: number;
    mousePosition: undefined | Position

    /** Constants */
    public height = 0;
    public sidebarInnerStart = 0

    public recalculateConstants() {
        this.constants = this.getConstants()

        this.height = window.innerHeight * RESOLUTION

        this.sidebarInnerStart = this.constants.sidebarStart + this.constants.sidebarPadding

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

    renderHexagon(pos: Position, options?: RenderHexagonOptions) {
        const {
            visible, clipPoints
        } = this.perspective.getTileRenderingConstants(pos, this.constants);

        if (!visible)
            return

        this.ctx.beginPath()
        this.ctx.strokeStyle = options.stroke ?? "#000000"
        this.ctx.fillStyle = options.color ?? "#000000"

        this.ctx.lineWidth = (options.strokeWidth ?? 0) * this.constants.resolution
        this.ctx.moveTo(clipPoints[clipPoints.length - 1].x, clipPoints[clipPoints.length - 1].y)
        clipPoints.forEach(pos => this.ctx.lineTo(pos.x, pos.y))

        this.ctx.globalAlpha = options.opacity ?? 1;
        this.ctx.stroke()
        this.ctx.fill()
        this.ctx.globalAlpha = 1

        this.ctx.closePath()
    }
}
