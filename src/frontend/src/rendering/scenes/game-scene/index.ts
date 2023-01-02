import {RenderingConstants, Scene} from "../scene";
import {Perspective} from "../../perspective";
import {NextTurnButton} from "../../entities/buttons/next-turn-button";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import {GameState} from "models";
import {PathPlanning} from "./path-planning";
import {UnitEntity} from "../../entities/unit-entity";


export class GameScene extends Scene {

    private nextTurnButton: NextTurnButton = null

    private selectedEntity: UnitEntity;
    private pathPlanning = new PathPlanning();

    onStart(constants: RenderingConstants): null {
        this.turnBanner.title("Game Phase")
        this.nextTurnButton = new NextTurnButton(constants);

        VelvetDawn.map.tiles.forEach(x => x.isSpawnArea = false)

        return null
    }

    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants, timeDelta: number): undefined {
        this.renderTiles(ctx, perspective, constants)
        this.pathPlanning.render(ctx, perspective, constants, this.hoveredTile?.position)
        this.renderUnits(ctx, perspective, constants, timeDelta)

        ctx.fillStyle = "#000000"
        ctx.fillRect(constants.sidebarStart, 0, constants.sidebar, constants.height)

        this.turnBanner.render(ctx, perspective, constants)
        this.nextTurnButton.draw(ctx, perspective, constants, this.mousePosition)

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
            }
            else if (mapEntity) {
                this.selectedEntity = mapEntity;
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
            }

        } else {
            [this.nextTurnButton].forEach(button => {
                if (button.isHovered({x, y}))
                    button.performClick()
            })
        }

        return null
    }

    keyboardInput(event: KeyboardEvent): null {
        // Ready up
        if (event.key === "Enter") {
            this.nextTurnButton.performClick();
            event.preventDefault()
        }

        if (event.key === "Escape") {
            this.selectedEntity = undefined
            this.pathPlanning.clear()
            this.clickedTile = undefined
            event.preventDefault()
        }

        return null
    }

    onStateUpdate(state: GameState): null {
        // Recompute paths incase anything has changed in the state update
        this.pathPlanning.clear()
        if (this.selectedEntity
                && VelvetDawn.isPlayersTurn()
                && this.selectedEntity.player === VelvetDawn.loginDetails.username) {
            this.pathPlanning.computePaths(this.selectedEntity.getPosition(), this.selectedEntity.attributes['movement.remaining'] ?? 0)
        }

        return null
    }
}
