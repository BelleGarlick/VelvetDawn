import {VelvetDawn} from "../velvet-dawn/velvet-dawn";
import { Perspective } from "./perspective";
import {TileEntity} from "./entities/tile-entity";
import {SetupPhase} from "./phases/setup";


const SIDEBAR_WIDTH = 360


export class Renderer {

    private canvas: HTMLCanvasElement;

    private static instance: Renderer = new Renderer();
    private perspective = new Perspective();

    public static getInstance() {
        return this.instance;
    }

    // @ts-ignore
    public render() {
        if (!this.canvas) {
            return undefined
        }

        var ctx = this.canvas.getContext('2d');
        this.canvas.width = window.innerWidth
        this.canvas.height = window.innerHeight

        VelvetDawn.tileEntities.forEach(tile => {
            tile.render(ctx, this.perspective)
        })

        ctx.fillStyle = "#000000"
        ctx.fillRect(window.innerWidth - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, window.innerHeight)

        SetupPhase.getInstance().renderSidebar(ctx, {
            width: window.innerWidth,
            height: window.innerHeight,
            sidebar: SIDEBAR_WIDTH
        })

        requestAnimationFrame(() => {this.render()})
    }

    public setCanvas(canvasRef: HTMLCanvasElement) {
        this.canvas = canvasRef

        let mouseDown = false
        let mousePos = {x: 0, y: 0}
        this.canvas.onmousemove = (event) => {
            if (mouseDown) {
                this.perspective.xOffset += mousePos.x - event.pageX
                this.perspective.yOffset += mousePos.y - event.pageY
            }
            mousePos = {x: event.pageX, y: event.pageY}

            if (SetupPhase.getInstance().hoveredTile) {
                SetupPhase.getInstance().hoveredTile.hovered = false
            }
            SetupPhase.getInstance().hoveredTile = this.perspective.getTileFromMouse(mousePos.x, mousePos.y)
            SetupPhase.getInstance().hoveredTile.hovered = true
        }

        let mouseDownPos = {x: 0, y: 0}
        this.canvas.onmousedown = (event) => {
            mouseDown = true
            mouseDownPos = {x: event.pageX, y: event.pageY}
        }

        this.canvas.onmouseup = (event) => {
            mouseDown = false
            const distance = Math.hypot(event.pageY - mouseDownPos.y, event.pageX - mouseDownPos.x)
            if (distance < 10) {
                SetupPhase.getInstance().tileClicked()
            }
        }

        this.render()
    }
}
