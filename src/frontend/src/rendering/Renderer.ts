import {VelvetDawn} from "../velvet-dawn/velvet-dawn";
import { Perspective } from "./perspective";
import {SetupPhase} from "./scenes/setup";
import {RenderingConstants, Scene} from "./scenes/scene";
import {GameScene} from "./scenes/game-scene";
import {SpectatingScene} from "./scenes/spectating-scene";
import {RenderingFacade} from "./facade";


const RESOLUTION = 2


class DebugOptions {

    private lastRenderTime: number = 0
    private lastFrameEnd: number = 0
    private rates: number[] = []

    public update(frameStart: number, frameEnd: number) {
        this.lastRenderTime = frameEnd - frameStart;

        if (this.lastFrameEnd !== 0) {
            this.rates.push(frameEnd - this.lastFrameEnd)
        }
        this.lastFrameEnd = frameEnd

        if (this.rates.length > 100) {
            this.rates.shift()
        }
    }

    render(ctx: CanvasRenderingContext2D, constants: RenderingConstants) {
        const state = VelvetDawn.getState()
        let total = 0
        this.rates.forEach(x => total += x);
        total /= this.rates.length
        const renderRate = Math.round(total * 100) / 100;

        const framesPerSecond = Math.round(1000 / total * 100) / 100;

        ctx.fillStyle = "#ffffff"
        ctx.textBaseline = "bottom"
        ctx.textAlign = "left"
        ctx.font = "40px arial";
        ctx.fillText(`Render Times: ${this.lastRenderTime} ${renderRate} ${framesPerSecond}`, 10, constants.height - 10)
        ctx.fillText(`Attribute updates: ${state.attrChanges.length}`, 10, constants.height - 60)
    }

    public getLastRenderTime() {
        return this.lastRenderTime
    }
}


export class Renderer {

    private canvas: HTMLCanvasElement;

    private static instance: Renderer = new Renderer();
    private perspective = new Perspective();

    private scene: Scene = new SetupPhase();

    private debugOptions  = new DebugOptions();

    public facade = new RenderingFacade()

    public static getInstance() {
        return this.instance;
    }

    // @ts-ignore
    public render() {
        if (!this.canvas)
            return undefined

        const start = new Date().getTime()

        this.updateScene();

        const ctx = this.canvas.getContext('2d');
        this.canvas.width = window.innerWidth * RESOLUTION
        this.canvas.height = window.innerHeight * RESOLUTION
        this.canvas.style.width = window.innerWidth + "px"
        this.canvas.style.height = window.innerHeight + "px"

        this.facade.ctx = ctx;
        this.facade.perspective = this.perspective
        this.facade.timeDelta = this.debugOptions.getLastRenderTime() / 1000
        this.facade.recalculateConstants()

        ctx.fillStyle = "#66d9e8"
        ctx.fillRect(0, 0, this.facade.width, this.facade.height)


        this.scene.render(this.facade)

        this.debugOptions.render(ctx, this.facade.constants)

        const end = new Date().getTime()
        this.debugOptions.update(start, end);

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
            this.facade.mousePosition = mousePos

            if (this.scene.hoveredTile) {
                this.scene.hoveredTile.hovered = false
            }
            this.scene.hoveredTile = this.perspective.getTileFromMouse(mousePos.x, mousePos.y)
            this.scene.hoveredTile.hovered = true
        }

        this.canvas.onmouseleave = () => this.facade.mousePosition = undefined

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
                this.scene.clicked(this.facade.constants, evX, evY)
            }
        }

        document.addEventListener('keydown', (event) => {
            this.scene.keyboardInput(event)
        });


        this.render()
    }

    getScene(): Scene {
        return this.scene;
    }

    private updateScene() {
        this.facade.recalculateConstants()
        const phase = VelvetDawn.getState().phase

        // Check if the player is just spectating
        if (VelvetDawn.getPlayer().spectating) {
            if (!(this.scene instanceof SpectatingScene)) {
                this.scene = new SpectatingScene()
                this.scene.onStart(this.facade)
            }
        }

        else if (phase === "setup" && !(this.scene instanceof SetupPhase)) {
            this.scene = new SetupPhase()
            this.scene.onStart(this.facade)
        }

        else if (phase === "game" && !(this.scene instanceof GameScene)) {
            this.scene = new GameScene()
            this.scene.onStart(this.facade)
        }
    }

    static startScene() {
        const renderer = Renderer.getInstance()
        renderer.facade.recalculateConstants()
        renderer.getScene().onStart(renderer.facade)
    }
}
