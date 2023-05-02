import {RenderingConstants, Scene} from "../scene";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import {GameState} from "models";
import {PathPlanning} from "./path-planning";
import {UnitEntity} from "../../entities/unit-entity";
import {GameViewSidebar} from "./sidebar";
import {RenderingFacade} from "../../facade";
import {Combat} from "./combat";


export class GameScene extends Scene {

    private sidebar: GameViewSidebar

    private selectedEntity: UnitEntity;
    private pathPlanning = new PathPlanning();
    private combat = new Combat();

    /** Setup view components */
    onStart(facade: RenderingFacade): null {
        this.sidebar = new GameViewSidebar(facade.constants)
        this.turnBanner.title("Game Phase")

        return null
    }

    render(facade: RenderingFacade): undefined {
        this.renderTiles(facade)
        this.pathPlanning.render(facade, this.hoveredTile?.position)
        this.combat.render(facade, this.hoveredTile?.position)
        this.renderUnits(facade)

        this.turnBanner.render(facade)
        this.sidebar.setSelectedUnit(this.selectedEntity)
        this.sidebar.render(facade)

        return undefined;
    }

    clicked(constants: RenderingConstants, x: number, y: number): null {
        // Check if clicked in game or in sidebar
        if (x < constants.width - constants.sidebar) {
            if (this.clickedTile)
                this.clickedTile.selected = false;
            this.clickedTile = this.hoveredTile;
            this.clickedTile.selected = true;

            // TODO Check if can move to the tile or should fight it
            const mapEntity = VelvetDawn.map.getUnitAtPosition(this.clickedTile.position)
            if (mapEntity && mapEntity.player === VelvetDawn.loginDetails.username && VelvetDawn.isPlayersTurn()) {
                // This is for own clause, will need another clause for non-player owned entities
                this.selectedEntity = mapEntity;
                this.pathPlanning.computePaths(this.clickedTile.position, mapEntity.attributes['movement.remaining'] ?? 0)

                const combatRange = this.selectedEntity.attributes['combat.range'] ?? 1
                this.combat.getTargetablePositions(this.selectedEntity.getPosition(), combatRange)
            }
            else if (this.selectedEntity
                && VelvetDawn.isPlayersTurn()
                && this.selectedEntity.player === VelvetDawn.loginDetails.username
                && this.combat.isPointInRange(this.clickedTile.position)) {
                this.combat.attack(this.selectedEntity.instanceId, this.clickedTile.position)
            }
            else if (mapEntity) {
                this.selectedEntity = mapEntity;
                this.combat.clear()
                this.pathPlanning.clear()
            }
            else if (this.selectedEntity
                && VelvetDawn.isPlayersTurn()
                && this.selectedEntity.player === VelvetDawn.loginDetails.username
                && this.pathPlanning.isPointInRange(this.clickedTile.position)) {
                // TODO Check if the player owns this tile otherwise it'll be pointless
                this.pathPlanning.moveUnit(this.selectedEntity.instanceId, this.clickedTile.position)
            }
            else {
                this.selectedEntity = null
                this.pathPlanning.clear()
                this.combat.clear()
            }

        } else {
            this.sidebar.clicked({x: x, y: y})
        }

        return null
    }

    keyboardInput(event: KeyboardEvent): null {
        // Ready up
        if (event.key === "Enter") {
            this.sidebar.nextTurnButton.performClick();
            event.preventDefault()
        }

        if (event.key === "Escape") {
            this.selectedEntity = undefined
            this.pathPlanning.clear()
            this.combat.clear()
            this.clickedTile = undefined
            event.preventDefault()
        }

        return null
    }

    onStateUpdate(state: GameState): null {
        // Recompute paths incase anything has changed in the state update
        this.pathPlanning.clear()
        this.combat.clear()
        if (this.selectedEntity
                && VelvetDawn.isPlayersTurn()
                && this.selectedEntity.player === VelvetDawn.loginDetails.username) {
            this.pathPlanning.computePaths(this.selectedEntity.getPosition(), this.selectedEntity.attributes['movement.remaining'] ?? 0)

            const combatRange = this.selectedEntity.attributes['combat.range'] ?? 1
            this.combat.getTargetablePositions(this.selectedEntity.getPosition(), combatRange)
        }

        this.sidebar.onStateUpdate(state)

        return null
    }
}
