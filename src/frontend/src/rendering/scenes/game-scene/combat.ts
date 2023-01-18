import {Position} from "models";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";

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
                    if (unit.player !== VelvetDawn.getPlayer().team) {
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
}