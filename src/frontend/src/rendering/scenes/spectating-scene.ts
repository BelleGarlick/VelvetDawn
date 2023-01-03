import {RenderingConstants, Scene} from "./scene";
import {GameState} from "models";
import {RenderingFacade} from "../facade";


export class SpectatingScene extends Scene {

    render(facade: RenderingFacade): undefined {
        this.renderTiles(facade)
        this.renderUnits(facade)
        this.turnBanner.render(facade)

        return undefined;
    }

    onStart(facade: RenderingFacade): null {
        this.turnBanner.title("Spectating")

        return null
    }

    clicked(constants: RenderingConstants, x: number, y: number): null { return null }
    keyboardInput(event: KeyboardEvent): null { return null }
    onStateUpdate(state: GameState): undefined { return undefined; }
}
