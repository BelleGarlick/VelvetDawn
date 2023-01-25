import {Position} from "models";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import {RenderingFacade} from "../../facade";
import * as Api from "api";

/** Combats class for getting the list of positions
 * the selected unit can attack and calling the api
 * for combat related calls.
 */

export class Combat {

    private currentPosition: Position | undefined
    private currentRange: number = -1
    private targetablePosition: Set<Position> = new Set();

    /** Get all positions in targetable range
     *
     * This will return the cached value and only
     * recalculate if different.
     *
     * @param position The position to get units surrounding
     * @param range The maximum distance away.
     */
    getTargetablePositions(position: Position, range: number): Set<Position> {
        if (this.currentPosition?.x !== position.x || this.currentPosition?.x !== position.y || range !== this.currentRange) {
            this.clear()

            VelvetDawn.map
                .getUnitsInRange(position, range)
                .forEach(unit => {
                    if (unit.player !== VelvetDawn.getPlayer().name) {
                        this.targetablePosition.add(unit.getPosition());
                    }
                })
        }

        return this.targetablePosition;
    }

    /** Clear the combat targets cache */
    clear() {
        this.currentPosition = undefined
        this.currentRange = -1
        this.targetablePosition.clear()
    }

    render(facade: RenderingFacade, hoveredTilePosition: Position) {
        const { ctx, constants } = facade;
        this.targetablePosition.forEach(position => {
            const {
                visible, clipPoints
            } = facade.perspective.getTileRenderingConstants(position, facade.constants);

            if (!visible)
                return

            ctx.beginPath()
            ctx.strokeStyle = "#dd0000"
            ctx.fillStyle = "#dd0000"
            ctx.lineWidth = 3 * constants.resolution
            ctx.moveTo(clipPoints[clipPoints.length - 1].x, clipPoints[clipPoints.length - 1].y)
            clipPoints.forEach(pos => ctx.lineTo(pos.x, pos.y))
            ctx.stroke()

            ctx.globalAlpha = (hoveredTilePosition?.x === position.x && hoveredTilePosition?.y === position.y)
                ? 0.3
                : 0.15;
            ctx.fill()
            ctx.globalAlpha = 1

            ctx.closePath()
        })
    }

    isPointInRange(position: Position) {
        let found = false;

        this.targetablePosition.forEach(pos => {
            if (pos.x === position.x && pos.y === position.y)
                found = true
        })

        return found
    }

    attack(instanceId: string, position: Position) {
        // TODO Catch error and show in chat
        Api.combat.attack(instanceId, position).then(VelvetDawn.setState)
    }
}