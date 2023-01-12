import {VelvetDawn} from "../velvet-dawn/velvet-dawn";
import { Perspective } from "./perspective";
import {SetupPhase} from "./scenes/setup";
import {Scene} from "./scenes/scene";
import {GameScene} from "./scenes/game-scene";
import {SpectatingScene} from "./scenes/spectating-scene";
import {RenderingFacade} from "./facade";
import {Position} from "models/position";


const RESOLUTION = 2


export class Renderer {

    private canvas: HTMLCanvasElement;

    private static instance: Renderer = new Renderer();
    private perspective = new Perspective();

    private scene: Scene = new SetupPhase();

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
        this.facade.timeDelta = VelvetDawn.debug.getLastRenderTime() / 1000
        this.facade.recalculateConstants()

        ctx.fillStyle = "#66d9e8"
        ctx.fillRect(0, 0, this.facade.width, this.facade.height)


        this.scene.render(this.facade)

        VelvetDawn.debug.render(ctx, this.facade.constants)

        const end = new Date().getTime()
        VelvetDawn.debug.update(start, end);

        requestAnimationFrame(() => {this.render()})
    }

    public setCanvas(canvasRef: HTMLCanvasElement) {
        this.canvas = canvasRef

        let mousePos = {x: 0, y: 0}
        this.canvas.onmousemove = (event) => {
            if (!document.onmousemove) {
                const evX = event.pageX * RESOLUTION
                const evY = event.pageY * RESOLUTION

                mousePos = {x: evX, y: evY}
                this.facade.mousePosition = mousePos

                if (this.scene.hoveredTile) {
                    this.scene.hoveredTile.hovered = false
                }
                this.scene.hoveredTile = this.perspective.getTileFromMouse(mousePos.x, mousePos.y)
                this.scene.hoveredTile.hovered = true
            }
        }

        this.canvas.onmouseleave = () => this.facade.mousePosition = undefined

        let mouseDownPos: undefined | Position;
        this.canvas.onmousedown = (event) => {
            mousePos = {x: event.pageX * RESOLUTION, y: event.pageY * RESOLUTION}
            mouseDownPos = {x: event.pageX * RESOLUTION, y: event.pageY * RESOLUTION}

            document.onmousemove = (event) => {
                this.perspective.xOffset -= event.x * RESOLUTION - mousePos.x
                this.perspective.yOffset -= event.y * RESOLUTION - mousePos.y
                mousePos = {x: event.pageX * RESOLUTION, y: event.pageY * RESOLUTION}
            }

            document.onmouseup = () => {
                document.onmousemove = null
            }
        }

        this.canvas.onmouseup = (event) => {
            const evX = event.pageX * RESOLUTION
            const evY = event.pageY * RESOLUTION

            document.onmousemove = null
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
