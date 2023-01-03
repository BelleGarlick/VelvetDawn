import {RenderingConstants, Scene} from "../scene";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import {GameState} from "models/index";
import {RenderingFacade} from "../../facade";
import {SetupSceneSidebar} from "./sidebar";



export class SetupPhase extends Scene {

    private sidebar: SetupSceneSidebar

    render(facade: RenderingFacade): undefined {
        this.renderTiles(facade)
        this.renderUnits(facade)

        this.sidebar.render(facade)
        this.turnBanner.render(facade)

        return undefined;
    }

    onStart(facade: RenderingFacade): null {
        this.sidebar = new SetupSceneSidebar(facade);
        this.turnBanner.title("Setup Phase")

        VelvetDawn.getState().spawnArea.forEach((position) => {
            VelvetDawn.map.getTile(position).isSpawnArea = true
        })

        return null
    }

    clicked(constants: RenderingConstants, x: number, y: number): null {
        // Check if clicked in game or in sidebar
        if (x < constants.width - constants.sidebar) {
            if (this.clickedTile)
                this.clickedTile.selected = false;
            this.clickedTile = this.hoveredTile;
            this.clickedTile.selected = true;
            this.sidebar.clickedTile = this.hoveredTile

        } else {
            [
                ...this.sidebar.getVisibleButtons(),
                this.sidebar.nextTurnButton,
                this.sidebar.removeEntityButton
            ].forEach(button => {
                if (button.isHovered({x, y}))
                    button.performClick()
            })

            this.sidebar.tabButtons.setMousePos({x, y}).click()
        }

        return null
    }

    keyboardInput(event: KeyboardEvent): null {
        // Switch tab
        if (event.key === "Tab") {
            this.sidebar.toggleTab();
            event.preventDefault();
        }

        // Place item
        if (event.keyCode >= 49 && event.keyCode <= 57) {
            const buttonIndex = event.keyCode - 49;
            const buttons = this.sidebar.getVisibleButtons()
            if (buttonIndex < buttons.length)
                buttons[buttonIndex].performClick()
            event.preventDefault()
        }

        // Remove Item
        if (event.key === "Backspace") {
            this.sidebar.removeEntityButton.performClick();
            event.preventDefault()
        }

        // Ready up
        if (event.key === "Enter") {
            this.sidebar.nextTurnButton.performClick();
            event.preventDefault()
        }

        return null
    }

    onStateUpdate(state: GameState): undefined {
        return undefined;
    }
}
