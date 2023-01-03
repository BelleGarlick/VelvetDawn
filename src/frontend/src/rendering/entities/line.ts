import {Renderable} from "./renderable";
import {RenderingFacade} from "../facade";
import {Position} from "models/position";


export class Line extends Renderable {

    private startPos: Position = {x: 0, y: 0}
    private endPos: Position = {x: 0, y: 0}

    setLine(start: Position, end: Position) {
        this.startPos = start
        this.endPos = end
        return this
    }

    render({ctx, constants}: RenderingFacade): null {
        ctx.beginPath()

        ctx.strokeStyle = "#ffffff"
        ctx.lineWidth = 1.5 * constants.resolution
        ctx.moveTo(this.startPos.x, this.startPos.y)
        ctx.lineTo(this.endPos.x, this.endPos.y)
        ctx.stroke()

        ctx.closePath()

        return null;
    }

}
