import {Textures} from "../Textures";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {Entity} from "./entity";

// function pointy_hex_corner(center, size, i):
//     var angle_deg = 60 * i - 30°
//     var angle_rad = PI / 180 * angle_deg
//     return Point(center.x + size * cos(angle_rad),
//                  center.y + size * sin(angle_rad))

const SCALE = 50
const HEX_POINTS = [
    {x: SCALE * Math.cos(0), y: SCALE * Math.sin(0)},
    {x: SCALE * Math.cos(1 * Math.PI / 3), y: SCALE * Math.sin(1 * Math.PI / 3)},
    {x: SCALE * Math.cos(2 * Math.PI / 3), y: SCALE * Math.sin(2 * Math.PI / 3)},
    {x: SCALE * Math.cos(3 * Math.PI / 3), y: SCALE * Math.sin(3 * Math.PI / 3)},
    {x: SCALE * Math.cos(4 * Math.PI / 3), y: SCALE * Math.sin(4 * Math.PI / 3)},
    {x: SCALE * Math.cos(5 * Math.PI / 3), y: SCALE * Math.sin(5 * Math.PI / 3)},
]


export class UnitEntity extends Entity{

    private readonly x: number;
    private readonly y: number;

    constructor(id: string, x: number, y: number) {
        super(id)

        this.x = x;
        this.y = y
    }

    render(ctx: CanvasRenderingContext2D): null {
        const texture = Textures.assets[this.id]

        ctx.drawImage(texture, 0, 0)

        return null

        // const sprite = Sprite.from(Textures.assets[tileData.texture]);
        // sprite.anchor.set(0.5);
        // sprite.height = 100
        // sprite.width = 100
        //
        // // let's create a moving shape
        // this.mask = new Graphics();
        // this.mask.beginFill(0xC34288, 1);
        // this.mask.moveTo(HEX_POINTS[0].x, HEX_POINTS[0].y);
        // this.mask.lineTo(HEX_POINTS[1].x, HEX_POINTS[1].y);
        // this.mask.lineTo(HEX_POINTS[2].x, HEX_POINTS[2].y);
        // this.mask.lineTo(HEX_POINTS[3].x, HEX_POINTS[3].y);
        // this.mask.lineTo(HEX_POINTS[4].x, HEX_POINTS[4].y);
        // this.mask.lineTo(HEX_POINTS[5].x, HEX_POINTS[5].y);
        // this.mask.lineTo(HEX_POINTS[0].x, HEX_POINTS[0].y);
        // this.mask.endFill();
        // this.mask.lineStyle(0);
        // this.container.mask = this.mask;
        //
        // app.stage.addChild(this.mask);
        // this.container.addChild(sprite)
    }
}
