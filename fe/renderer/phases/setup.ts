import {PhaseScene, RenderingConstants} from "./phase";


export class SetupPhase extends PhaseScene {

    private static instance: SetupPhase = new SetupPhase();
    public static getInstance(): SetupPhase {
        return SetupPhase.instance;
    }

    private constructor() {
        super();
    }

    renderSidebar(ctx: CanvasRenderingContext2D, constants: RenderingConstants): undefined {
        if (this.hoveredTile) {
            ctx.font = "20px 'Velvet Dawn'";
            ctx.fillStyle = "#ff0000"
            ctx.fillText(this.hoveredTile.id.toString(), constants.width - constants.sidebar, 100)
        }

        return undefined;
    }

    tileClicked() {
        if (this.clickedTile)
            this.clickedTile.selected = false;
        this.clickedTile = this.hoveredTile;
        this.clickedTile.selected = true;
    }
}
