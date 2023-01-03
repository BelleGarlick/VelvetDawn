import {Entity} from "./entity";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {Textures} from "../Textures";
import {Position} from "models";
import * as geometry from '../../geometry'
import {RenderingFacade} from "../facade";

export class UnitEntity extends Entity {

    public readonly player: string

    private position: Position = undefined;
    private lastPosition: Position | undefined = undefined;
    private portion: number = 1

    public attributes: { [key: string]: any } = {}

    constructor(id: number, entityId: string, player: string) {
        super(id, entityId)

        this.player = player
    }

    render(facade: RenderingFacade): null {
        const entity = VelvetDawn.datapacks.entities[this.entityId]
        const texture = Textures.get(entity.textures.background)

        facade.ctx.fillStyle = "#000000"
        const size = facade.perspective.getUnitSize()

        let tilePosition = facade.perspective.getTileCoordinates(this.position)
        if (this.lastPosition) {
            let lastPos = facade.perspective.getTileCoordinates(this.lastPosition)

            const delta = geometry.sub(tilePosition, lastPos)
            const distance = geometry.length(delta)
            const frameDistance = 5000 * facade.constants.resolution * facade.timeDelta
            const portion = frameDistance / distance
            this.portion += portion

            tilePosition = geometry.add(lastPos, geometry.multiply(delta, this.portion))

            if (this.portion > 0.99) {
                this.lastPosition = undefined
            }
        }

        facade.ctx.drawImage(
            texture,
            0, 0,
            texture.width, texture.height,
            tilePosition.x - size / 2, tilePosition.y - size / 2, size, size
        )

        return null
    }

    setPosition(position: Position) {
        if (this.position === undefined
            || this.position.x !== position.x
            || this.position.y !== position.y) {
            this.lastPosition = this.position
            this.position = position
            this.portion = 0
        }
    }

    getPosition() {
        return this.position
    }
}
