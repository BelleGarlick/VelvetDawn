import { TileEntity } from "rendering/entities/tile-entity"
import { VelvetDawn } from "velvet-dawn/velvet-dawn"
import {RenderingConstants} from "./scenes/scene";
import {Position} from "models";

const TileRadius = 110
const TileHeight = Math.pow(3, 1/2) * TileRadius
const TileWidth = 2 * TileRadius
const TileSpacingX = TileWidth * 0.75
const TileSpacingY = TileHeight


export class Perspective {

    xOffset = 100
    yOffset = 100

    warp({ x, y } : { x: number, y: number }) {
        return {
            x: x - this.xOffset,
            y: y - this.yOffset
        }
    }

    unwarp({ x, y }: Position): Position {
        return {
            x: x + this.xOffset,
            y: y + this.yOffset
        }
    }

    public getTileCoordinates({x, y}: Position): Position {
        return this.warp({
            x: x * TileSpacingX,
            y: y * TileSpacingY + (x % 2 * TileHeight / 2)
        })
    }

    getTileRenderingConstants(position: Position, constants: RenderingConstants) {
        const { x: tilePosX, y: tilePosY } = this.getTileCoordinates(position)

        const clipPoints = [
            {x: tilePosX + TileRadius * Math.cos(0), y: tilePosY + TileRadius * Math.sin(0)},
            {x: tilePosX + TileRadius * Math.cos(1 * Math.PI / 3), y: tilePosY + TileRadius * Math.sin(1 * Math.PI / 3)},
            {x: tilePosX + TileRadius * Math.cos(2 * Math.PI / 3), y: tilePosY + TileRadius * Math.sin(2 * Math.PI / 3)},
            {x: tilePosX + TileRadius * Math.cos(3 * Math.PI / 3), y: tilePosY + TileRadius * Math.sin(3 * Math.PI / 3)},
            {x: tilePosX + TileRadius * Math.cos(4 * Math.PI / 3), y: tilePosY + TileRadius * Math.sin(4 * Math.PI / 3)},
            {x: tilePosX + TileRadius * Math.cos(5 * Math.PI / 3), y: tilePosY + TileRadius * Math.sin(5 * Math.PI / 3)},
        ]

        const visible = (
            tilePosX > -TileRadius &&
            tilePosX < constants.width + TileRadius &&
            tilePosY > -TileRadius &&
            tilePosY < constants.height + TileRadius
        );

        return {
            visible: visible,
            clipPoints: clipPoints,
            imageStart: tilePosX - TileRadius,
            imageEnd: tilePosY - TileRadius,
            imageWidth: 2 * TileRadius,
            imageHeight: 2 * TileRadius
        }
    }

    getTileFromMouse(mX: number, mY: number): TileEntity | undefined {
        const {x, y} = this.unwarp({x: mX, y: mY})
        const tileX = Math.ceil((x - TileRadius) / TileSpacingX)
        const tileY = Math.ceil((y - TileRadius) / TileSpacingY)

        const possibleTiles = [
            VelvetDawn.map.getTile({x: tileX, y: tileY}),
            ...VelvetDawn.map.getNeighbourTiles({x: tileX, y: tileY})
        ]
        let tile: TileEntity = undefined
        let distance = 1_000_000

        possibleTiles.forEach(cTile => {
            const { x, y } = this.getTileCoordinates(cTile.position)
            const cDistance = Math.hypot(y - mY, x - mX);

            if (cDistance < distance) {
                distance = cDistance
                tile = cTile;
            }
        })

        return tile
    }

    getUnitSize(): number {
        // 0.6 * TileDiameter
        return 2 * TileRadius * 0.6;
    }

    public computeHexPoints(width: number, height: number) {
        return [
            {x: width, y: height / 2},
            {x: width - (height / 2) * Math.cos(Math.PI / 3), y: height},
            {x: - (height / 2) * Math.cos(2 * Math.PI / 3), y: height},
            {x: 0, y: height / 2},
            {x: - (height / 2) * Math.cos(4 * Math.PI / 3), y: 0},
            {x: width - (height / 2) * Math.cos(5 * Math.PI / 3), y: 0},
        ]
    }
}
