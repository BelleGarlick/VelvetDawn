import {Position} from "models";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import {RenderingFacade} from "../../facade";
import * as Api from "api";
import {UnitEntity} from "../../entities/unit-entity";
import {PositionSet} from "../../../velvet-dawn/position-set";

/** Combats class for getting the list of positions
 * the selected unit can attack and calling the api
 * for combat related calls.
 */

export class Combat {

    private currentPosition: Position | undefined
    private currentRange: number = -1
    private targetablePosition = new PositionSet();

    /** Get all positions in targetable range
     *
     * This will return the cached value and only
     * recalculate if different.
     *
     * @param position The position to get units surrounding
     * @param range The maximum distance away.
     */
    getTargetablePositions(position: Position, range: number): Position[] {
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

        return this.targetablePosition.items();
    }

    /** Clear the combat targets cache */
    clear() {
        this.currentPosition = undefined
        this.currentRange = -1
        this.targetablePosition.clear()
    }

    render(facade: RenderingFacade, hoveredTilePosition: Position, instance: UnitEntity) {
        this.targetablePosition.items().forEach(position => {
            if (position.x == hoveredTilePosition.x && position.y == hoveredTilePosition.y) {
                var positions = VelvetDawn.map.getTilesInRange(position, instance.attributes['combat.blast-radius'] ?? 0);

                positions.forEach(pos => {
                    facade.renderHexagon(pos, {
                        color: '#ff0000',
                        opacity: 0.3
                    })
                })
            }

            facade.renderHexagon(position, {
                color: "#dd0000",
                stroke: {color: "#dd0000", width: 3},
                opacity: (hoveredTilePosition?.x === position.x && hoveredTilePosition?.y === position.y)
                    ? 0.3
                    : 0.15
            })
        })
    }

    isPointInRange(position: Position) {
        let found = false;

        this.targetablePosition.items().forEach(pos => {
            if (pos.x === position.x && pos.y === position.y)
                found = true
        })

        return found
    }

    attack(instanceId: string, position: Position) {
        // TODO Catch error and show in chat
        Api.combat.attack(instanceId, position)
            .then(VelvetDawn.setState)
    }
}