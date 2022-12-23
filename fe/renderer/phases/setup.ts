import {Scene, RenderingConstants} from "./scene";
import {Button} from "../entities/button";
import {Perspective} from "../perspective";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import * as Api from 'api'


export class SetupPhase extends Scene {

    private buttons: Button[] = []

    renderSidebar(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): undefined {
        const sidebarStart = constants.width - constants.sidebar;

        if (this.hoveredTile) {
            ctx.font = "20px 'Velvet Dawn'";
            ctx.fillStyle = "#ff0000"
            ctx.fillText(this.hoveredTile.entityId.toString(), sidebarStart, 100)
        }

        if (this.clickedTile) {

            this.buttons.forEach((button, i) => {
                const x = sidebarStart + constants.sidebarPadding;
                const y = 120 + i * 110;
                button.setPos(x, y).render(ctx, perspective)
            })
        }

        return undefined;
    }

    tileClicked() {
        if (this.clickedTile)
            this.clickedTile.selected = false;
        this.clickedTile = this.hoveredTile;
        this.clickedTile.selected = true;
    }

    onStart(constants: RenderingConstants): null {
        const sidebarStart = constants.width - constants.sidebar;

        Object.keys(VelvetDawn.getState().setup.units).forEach((key, i) => {
            const unit = VelvetDawn.datapacks.entities[key];
            console.log("Creating key " + key)
            this.buttons.push(
                new Button(
                    unit.name,
                    sidebarStart + constants.sidebarPadding,
                    120 + i * 110,
                    constants.sidebar - constants.sidebarPadding * 2,
                    100,
                ).onClick(() => {
                    console.log(key)
                    Api.setup.placeEntity(key, this.clickedTile.x, this.clickedTile.y).then(x => {
                        VelvetDawn.setState(x)
                    })
                })
            );
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

        } else {
            this.buttons.forEach(button => {
                if (x >= button.x
                    && x <= button.x + button.width
                    && y >= button.y
                    && y <= button.y + button.height) {
                    button.performClick()
                }
            })
        }

        return null
    }
}
