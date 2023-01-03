import {Textures} from "../Textures";
import {Entity} from "./entity";
import {Position} from "models";
import {RenderingFacade} from "../facade";


export enum Highlight {
    None,
    Green
}


export class TileEntity extends Entity {

    public readonly position: Position;

    public highlight = Highlight.None

    public hovered = false
    public selected = false;

    public isSpawnArea: boolean = false

    public attributes: { [key: string]: any } = {}

    constructor(instanceId: number, tileId: string, position: Position) {
        super(instanceId, tileId)

        this.position = position
    }

    render(facade: RenderingFacade): null {
        const {
            visible, imageStart, imageEnd, clipPoints, imageWidth, imageHeight
        } = facade.perspective.getTileRenderingConstants(this.position, facade.constants);

        if (!visible)
            return

        facade.ctx.save();

        // Create Hexagon to clip the image
        facade.ctx.beginPath();
        facade.ctx.moveTo(clipPoints[5].x, clipPoints[5].y);
        clipPoints.forEach(({x, y}) => {
            facade.ctx.lineTo(x, y);
        })
        facade.ctx.closePath();
        facade.ctx.clip();

        if (this.isSpawnArea) {
            facade.ctx.fillStyle = "#00ff00"
            facade.ctx.fillRect(imageStart, imageEnd, imageHeight, imageHeight)
        }

        facade.ctx.globalAlpha = this.isSpawnArea ? 0.5 : 1
        facade.ctx.fillStyle = this.attributes['texture.color'] ?? "#ff6699"
        facade.ctx.fillRect(imageStart, imageEnd, imageHeight, imageHeight)

        // Render texture
        const backgroundTexture = this.attributes['texture.background']
        if (backgroundTexture) {
            const texture = Textures.get(backgroundTexture)
            facade.ctx.drawImage(
                texture,
                0, 0,
                texture.width, texture.height,
                imageStart, imageEnd,
                imageWidth, imageHeight
            )
        }
        facade.ctx.globalAlpha = 1

        if (this.hovered) {
            facade.ctx.strokeStyle = "black"
            facade.ctx.lineWidth = 5
            facade.ctx.beginPath();
            facade.ctx.moveTo(clipPoints[5].x, clipPoints[5].y);
            clipPoints.forEach(({x, y}) => facade.ctx.lineTo(x, y));
            facade.ctx.closePath();
            facade.ctx.stroke();
        }

        if (this.selected) {
            facade.ctx.strokeStyle = "black"
            facade.ctx.lineWidth = 10
            facade.ctx.beginPath();
            facade.ctx.moveTo(clipPoints[5].x, clipPoints[5].y);
            clipPoints.forEach(({x, y}) => facade.ctx.lineTo(x, y));
            facade.ctx.closePath();
            facade.ctx.stroke();
        }

        facade.ctx.restore();

        return null
    }
}
