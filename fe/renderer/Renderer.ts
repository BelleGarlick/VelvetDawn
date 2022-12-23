import {VelvetDawn} from "../velvet-dawn/velvet-dawn";
import { Perspective } from "./perspective";
import {SetupPhase} from "./phases/setup";
import {Scene} from "./phases/scene";


const SIDEBAR_WIDTH = 700
const RESOLUTION = 2


export class Renderer {

    private canvas: HTMLCanvasElement;

    private static instance: Renderer = new Renderer();
    private perspective = new Perspective();

    private scene: Scene = new SetupPhase();

    public static getInstance() {
        return this.instance;
    }

    // @ts-ignore
    public render() {
        if (!this.canvas) {
            return undefined
        }

        var ctx = this.canvas.getContext('2d');
        this.canvas.width = window.innerWidth * RESOLUTION
        this.canvas.height = window.innerHeight * RESOLUTION
        this.canvas.style.width = window.innerWidth + "px"
        this.canvas.style.height = window.innerHeight + "px"

        const constants = Renderer.getConstants()

        VelvetDawn.tileEntities.forEach(tile => {
            tile.render(ctx, this.perspective, constants)
        })

        // TODO Entity culling and updating if pos is outside window + 1 border for animating
        Object.keys(VelvetDawn.unitsDict).forEach(entityId => {
            VelvetDawn.unitsDict[entityId].render(ctx, this.perspective, constants)
        })

        ctx.fillStyle = "#000000"
        ctx.fillRect(constants.width - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, constants.height)

        this.scene.renderSidebar(ctx, this.perspective, Renderer.getConstants())

        requestAnimationFrame(() => {this.render()})
    }

    public setCanvas(canvasRef: HTMLCanvasElement) {
        this.canvas = canvasRef

        let mouseDown = false
        let mousePos = {x: 0, y: 0}
        this.canvas.onmousemove = (event) => {
            const evX = event.pageX * RESOLUTION
            const evY = event.pageY * RESOLUTION

            if (mouseDown) {
                this.perspective.xOffset += mousePos.x - evX
                this.perspective.yOffset += mousePos.y - evY
            }
            mousePos = {x: evX, y: evY}

            if (this.scene.hoveredTile) {
                this.scene.hoveredTile.hovered = false
            }
            this.scene.hoveredTile = this.perspective.getTileFromMouse(mousePos.x, mousePos.y)
            this.scene.hoveredTile.hovered = true
        }

        let mouseDownPos = {x: 0, y: 0}
        this.canvas.onmousedown = (event) => {
            mouseDown = true
            mouseDownPos = {x: event.pageX * RESOLUTION, y: event.pageY * RESOLUTION}
        }

        this.canvas.onmouseup = (event) => {
            const evX = event.pageX * RESOLUTION
            const evY = event.pageY * RESOLUTION

            mouseDown = false
            const distance = Math.hypot(evY - mouseDownPos.y, evX - mouseDownPos.x)
            if (distance < 10) {
                this.scene.clicked(Renderer.getConstants(), evX, evY)
            }
        }

        this.render()
    }

    getScene(): Scene {
        return this.scene;
    }

    static getConstants() {
        return {
            width: window.innerWidth * RESOLUTION,
            height: window.innerHeight * RESOLUTION,
            sidebar: SIDEBAR_WIDTH,
            sidebarPadding: 10
        }
    }
}
