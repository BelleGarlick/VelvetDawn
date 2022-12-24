import {Perspective} from "../../perspective";
import {ButtonBase} from "./button-base";


export class Button extends ButtonBase {

    public width: number
    public height: number


    constructor(width: number, height: number) {
        super();

        this.width = width
        this.height = height
    }

    public render(ctx: CanvasRenderingContext2D, perspective: Perspective): null {
        ctx.fillStyle = "#ff0000"
        ctx.fillRect(this.x, this.y, this.width, this.height)

        ctx.font = "40px 'Velvet Dawn'";
        ctx.fillStyle = this._textColor
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this._text, this.x + this.width / 2, this.y + this.height / 2)

        return null
    }
}
