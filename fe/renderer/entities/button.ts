import {Renderable} from "./renderable";
import {Perspective} from "../perspective";


export class Button extends Renderable {

    public text: string

    public x: number
    public y: number
    public width: number
    public height: number

    private _textColor: string = "#000000"

    private func?: () => void = undefined

    constructor(text: string, x: number, y: number, width: number, height: number) {
        super();

        this.text = text
        this.x = x
        this.y = y
        this.width = width
        this.height = height
    }

    textColor(color: string) {
        this._textColor = color
        return this
    }

    public render(ctx: CanvasRenderingContext2D, perspective: Perspective): null {
        ctx.fillStyle = "#ff0000"
        ctx.fillRect(this.x, this.y, this.width, this.height)

        ctx.font = "40px 'Velvet Dawn'";
        ctx.fillStyle = "#000000"
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.text, this.x + this.width / 2, this.y + this.height / 2)

        return null
    }

    public onClick(func: () => void) {
        this.func = func
        return this
    }

    public performClick() {
        if (this.func)
            this.func()
    }

    setPos(x: number, y: number) {
        this.x = x
        this.y = y
        return this
    }
}
