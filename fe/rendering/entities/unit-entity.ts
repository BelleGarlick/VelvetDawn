import {Entity} from "./entity";
import {Perspective} from "../perspective";
import {RenderingConstants} from "../phases/scene";
import {EntityInstance} from "models/entityInstance";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {Textures} from "../Textures";

export class UnitEntity extends Entity {

    private x: number;
    private y: number;

    private constructor(id: number, entityId: string, x: number, y: number) {
        super(id, entityId)

        this.x = x;
        this.y = y
    }

    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): null {
        // const texture = Textures.get(this.id)
        // console.log(VelvetDawn.)
        const entity = VelvetDawn.datapacks.entities[this.entityId]
        const texture = Textures.get(entity.textures.background)

        const {x, y} = perspective.getTileCoordinates(this.x, this.y)

        ctx.fillStyle = "#000000"
        const size = perspective.getUnitSize()

        ctx.drawImage(
            texture,
            0, 0,
            texture.width, texture.height,
            x - size / 2, y - size / 2, size, size
        )

        ctx.fill()

        return null
    }

    setPosition(position: { x: number; y: number }) {
        this.x = position.x;
        this.y = position.y;
    }

    static fromServerInstance(serverEntity: EntityInstance): UnitEntity {
        return new UnitEntity(
            serverEntity.id,
            serverEntity.entity,
            serverEntity.position.x,
            serverEntity.position.y
        );
    }
}
