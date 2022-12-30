import {RenderingConstants, Scene} from "./scene";
import {Perspective} from "../perspective";
import {GameState} from "models";


export class SpectatingScene extends Scene {

    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): undefined {
        this.turnBanner.render(ctx, perspective, constants)

        return undefined;
    }

    onStart(constants: RenderingConstants): null {
        this.turnBanner.title("Spectating")

        return null
    }

    clicked(constants: RenderingConstants, x: number, y: number): null {
        return null
    }

    keyboardInput(event: KeyboardEvent): null {
        return null
    }

    onStateUpdate(state: GameState): undefined {
        return undefined;
    }
}
