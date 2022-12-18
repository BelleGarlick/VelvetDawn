import { Perspective } from "renderer/perspective";
import {Textures} from "../Textures";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {Entity} from "./entity";


export class TileEntity extends Entity{

    public readonly x: number;
    public readonly y: number;

    public hovered = false
    public selected = false;

    constructor(id: string, x: number, y: number) {
        super(id)

        this.x = x;
        this.y = y
    }

    render(ctx: CanvasRenderingContext2D, perspective: Perspective): null {
        const {
            visible, imageStart, imageEnd, clipPoints, imageWidth, imageHeight
        } = perspective.getTileRenderingConstants(this.x, this.y);

        if (!visible)
            return

        const tileData = VelvetDawn.tiles[this.id]
        const texture = Textures.assets[tileData.texture]

        ctx.save();

        // Create Hexagon to clip the image
        ctx.beginPath();
        ctx.moveTo(clipPoints[5].x, clipPoints[5].y);
        clipPoints.forEach(({x, y}) => {
            ctx.lineTo(x, y);
        })
        ctx.closePath();
        ctx.clip();

        if (this.selected) {
            ctx.fillStyle = "#00ff00"
            ctx.fillRect(imageStart, imageEnd, imageHeight, imageHeight)
        }

        // Render texture
        ctx.globalAlpha = (this.hovered || this.selected) ? 0.5 : 1
        ctx.drawImage(
            texture,
            0, 0,
            texture.width, texture.height,
            imageStart, imageEnd,
            imageWidth, imageHeight
        )

        ctx.restore();

        return null
    }
}
