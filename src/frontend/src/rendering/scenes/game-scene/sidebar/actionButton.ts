import {Position} from "models";
import {ButtonBase} from "../../../entities/buttons/button-base";
import {RenderingFacade} from "../../../facade";
import {Textures} from "../../../Textures";


export class ActionButton extends ButtonBase {

    private _hexPoints: Position[] = []

    private readonly _description: string = ""
    private invalidReason: string = ""
    private isUsed: boolean = false

    constructor(description: string) {
        super();
        this.textColor("#ffffff")
        this._description = description && description.length > 0 ? description : "No description given."
    }

    public render(facade: RenderingFacade): null {
        if (!this._enabled) {
            facade.ctx.globalAlpha = 0.5
        }

        if (this._hexPoints.length === 0) {
            this._hexPoints = facade.perspective.computeHexPoints(this.width, this.height);
        }

        facade.ctx.beginPath();
        facade.ctx.moveTo(this._hexPoints[5].x + this.x, this._hexPoints[5].y + this.y);
        this._hexPoints.forEach(({x, y}) => {
            facade.ctx.lineTo(this.x + x,this.y + y);
        })
        facade.ctx.closePath();
        facade.ctx.fillStyle = this._hovered ? this._backgroundHoverColor : this._backgroundColor
        if (!this._enabled)
            facade.ctx.fillStyle = this._backgroundColor

        facade.ctx.fill();
        facade.ctx.strokeStyle = "#ffffff"
        facade.ctx.lineWidth = 2
        facade.ctx.stroke();

        const texture = Textures.get(this.isUsed ? 'base:textures.ui.icons.tick.png' : this._icon)
        let imageWidth = this.height * 0.6;
        facade.ctx.drawImage(
            texture,
            0, 0,
            texture.width, texture.height,
            this.x + this.height / 3, this.y + this.height / 2 - imageWidth / 2,
            imageWidth, imageWidth
        )

        imageWidth += this.height / 6

        facade.ctx.fillStyle = this._textColor
        facade.ctx.textBaseline = 'middle';
        facade.ctx.textAlign = 'left';

        facade.ctx.font = "30px 'Velvet Dawn'";
        facade.ctx.fillText(this._text, this.x + this.height / 3 + imageWidth, this.y + this.height / 3)
        facade.ctx.font = "25px 'Velvet Dawn'";
        if (this.invalidReason)
            facade.ctx.fillStyle = "#dd0000"
        facade.ctx.fillText(this.invalidReason ?? this._description, this.x + this.height / 3 + imageWidth, this.y + 2 * this.height / 3)

        facade.ctx.closePath()
        facade.ctx.globalAlpha = 1

        return null
    }

    setReason(reason: string | undefined) {
        this.invalidReason = reason;
        return this
    }

    used() {
        this.isUsed = true
        this.enabled(false)
        return this
    }
}
