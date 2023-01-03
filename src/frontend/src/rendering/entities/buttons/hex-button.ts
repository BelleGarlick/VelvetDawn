import {ButtonBase, TextAlign} from "./button-base";
import {Position} from "models";
import {Textures} from "../../Textures";
import {RenderingFacade} from "../../facade";


export class HexButton extends ButtonBase {

    private _hexPoints: Position[] = []

    constructor(width: number, height: number) {
        super();

        this.width = width
        this.height = height
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

        let imageWidth = 0
        if (this._icon) {
            const texture = Textures.get(this._icon)
            imageWidth = this.height * 0.6;
            facade.ctx.drawImage(
                texture,
                0, 0,
                texture.width, texture.height,
                this.x + this.height / 3, this.y + this.height / 2 - imageWidth / 2,
                imageWidth, imageWidth
            )

            imageWidth += this.height / 6
        }

        facade.ctx.font = "40px 'Velvet Dawn'";
        facade.ctx.fillStyle = this._textColor

        facade.ctx.textBaseline = 'middle';
        if (this._textAlign === TextAlign.Left) {
            facade.ctx.textAlign = 'left';
            facade.ctx.fillText(this._text, this.x + this.height / 3 + imageWidth, this.y + this.height / 2)
        }
        if (this._textAlign === TextAlign.Center) {
            facade.ctx.textAlign = 'center';
            facade.ctx.fillText(this._text, this.x + this.width / 2, this.y + this.height / 2)
        }
        if (this._textAlign === TextAlign.Right) {
            facade.ctx.textAlign = 'right';
            facade.ctx.fillText(this._text, this.x + this.width - this.height / 3, this.y + this.height / 2)
        }
        facade.ctx.closePath()
        facade.ctx.globalAlpha = 1

        return null
    }
}
