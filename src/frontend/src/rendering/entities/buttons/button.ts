import {ButtonBase} from "./button-base";
import {RenderingFacade} from "../../facade";


export class Button extends ButtonBase {

    public width: number
    public height: number


    constructor(width: number, height: number) {
        super();

        this.width = width
        this.height = height
    }

    public render(facade: RenderingFacade): null {
        facade.ctx.beginPath()
        facade.ctx.fillStyle = "#ff0000"
        facade.ctx.fillRect(this.x, this.y, this.width, this.height)

        facade.ctx.font = "40px 'Velvet Dawn'";
        facade.ctx.fillStyle = this._textColor
        facade.ctx.textAlign = 'center';
        facade.ctx.textBaseline = 'middle';
        facade.ctx.fillText(this._text, this.x + this.width / 2, this.y + this.height / 2)
        facade.ctx.closePath()

        return null
    }
}
