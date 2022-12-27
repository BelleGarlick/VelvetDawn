import {RenderingConstants, Scene} from "./scene";
import {Perspective} from "../perspective";
import {NextTurnButton} from "../entities/buttons/next-turn-button";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";


export class GamePhase extends Scene {

    private nextTurnButton: NextTurnButton = null

    onStart(constants: RenderingConstants): null {
        this.turnBanner.title("Game Phase")
        this.nextTurnButton = new NextTurnButton(constants);

        if (VelvetDawn.map.length > 0 && VelvetDawn.getState().spawnArea.length > 0)
            VelvetDawn.tileEntities.forEach(x => x.isSpawnArea = false)


        return null
    }

    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): undefined {
        this.nextTurnButton.draw(ctx, perspective, constants, this.mousePosition)
        this.turnBanner.render(ctx, perspective, constants)

        return undefined;
    }

    clicked(constants: RenderingConstants, x: number, y: number): null {
        // Check if clicked in game or in sidebar
        if (x < constants.width - constants.sidebar) {
            if (this.clickedTile)
                this.clickedTile.selected = false;
            this.clickedTile = this.hoveredTile;
            this.clickedTile.selected = true;

        } else {
            [
                this.nextTurnButton
            ].forEach(button => {
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

        return null
    }
}
