import {Renderable} from "./renderable";
import {RenderingFacade} from "../facade";
import {Position} from "models/position";


export class Rectangle extends Renderable {

    private color = "black"
    private stroke = "#ffffff"
    private pos: Position = {x: 0, y: 0}
    private size: Position = {x: 0, y: 0}

    setLine(pos: Position, size: Position) {
        this.pos = pos
        this.size = size
        return this
    }

    render({ctx, constants}: RenderingFacade): null {
        ctx.beginPath()
        ctx.strokeStyle = this.stroke
        ctx.lineWidth = 3 * constants.resolution
        ctx.rect(this.pos.x, this.pos.y, this.size.x, this.size.y)
        ctx.stroke()
        ctx.closePath()

        ctx.beginPath()
        ctx.fillStyle = this.color
        ctx.fillRect(this.pos.x, this.pos.y, this.size.x, this.size.y)
        ctx.closePath()

        ctx.restore()

        return null;
    }

    setFrame(posX: number, posY: number, width: number, height: number) {
        this.pos.x = posX
        this.pos.y = posY
        this.size.x = width
        this.size.y = height
        return this;
    }
}
