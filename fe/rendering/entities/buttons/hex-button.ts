import {Perspective} from "../../perspective";
import {ButtonBase, TextAlign} from "./button-base";
import {Position} from "models/position";
import {Textures} from "../../Textures";


export class HexButton extends ButtonBase {

    public width: number
    public height: number

    private _hexPoints: Position[] = []

    constructor(width: number, height: number) {
        super();

        this.width = width
        this.height = height

        this.computeHexPoints()
    }

    public render(ctx: CanvasRenderingContext2D, perspective: Perspective): null {
        if (!this._enabled) {
            ctx.globalAlpha = 0.5
        }

        ctx.beginPath();
        ctx.moveTo(this._hexPoints[5].x + this.x, this._hexPoints[5].y + this.y);
        this._hexPoints.forEach(({x, y}) => {
            ctx.lineTo(this.x + x,this.y + y);
        })
        ctx.closePath();
        ctx.fillStyle = this._backgroundColor
        ctx.fill();
        ctx.strokeStyle = "#ffffff"
        ctx.lineWidth = 2
        ctx.stroke();

        let imageWidth = 0
        if (this._icon) {
            const texture = Textures.assets[this._icon]
            imageWidth = this.height * 0.6;
            ctx.drawImage(
                texture,
                0, 0,
                texture.width, texture.height,
                this.x + this.height / 3, this.y + this.height / 2 - imageWidth / 2,
                imageWidth, imageWidth
            )

            imageWidth += this.height / 6
        }

        ctx.font = "40px 'Velvet Dawn'";
        ctx.fillStyle = this._textColor

        ctx.textBaseline = 'middle';
        if (this._textAlign === TextAlign.Left) {
            ctx.textAlign = 'left';
            ctx.fillText(this._text, this.x + this.height / 3 + imageWidth, this.y + this.height / 2)
        }
        if (this._textAlign === TextAlign.Center) {
            ctx.textAlign = 'center';
            ctx.fillText(this._text, this.x + this.width / 2, this.y + this.height / 2)
        }
        if (this._textAlign === TextAlign.Right) {
            ctx.textAlign = 'right';
            ctx.fillText(this._text, this.x + this.width - this.height / 3, this.y + this.height / 2)
        }

        ctx.globalAlpha = 1

        return null
    }

    private computeHexPoints() {
        this._hexPoints = [
            {x: this.width, y: this.height / 2},
            {x: this.width - (this.height / 2) * Math.cos(Math.PI / 3), y: this.height},
            {x: - (this.height / 2) * Math.cos(2 * Math.PI / 3), y: this.height},
            {x: 0, y: this.height / 2},
            {x: - (this.height / 2) * Math.cos(4 * Math.PI / 3), y: 0},
            {x: this.width - (this.height / 2) * Math.cos(5 * Math.PI / 3), y: 0},
        ]
    }
}
