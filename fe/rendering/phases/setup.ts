import {RenderingConstants, Scene} from "./scene";
import {Perspective} from "../perspective";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import * as Api from 'api'
import {Button, HexButton, TextAlign} from "../entities/buttons"
import {Position} from "models/position";


class IdHexButton extends HexButton {
    public id: string = null
}


export class SetupPhase extends Scene {

    private allButtons: Button[] = []

    private buttons: IdHexButton[] = []
    private bannerButton: Button = null
    private nextTurnButton: Button = null
    private removeEntityButton: Button = null

    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): undefined {
        const sidebarStart = constants.width - constants.sidebar;
        const setup = VelvetDawn.getState().setup

        if (this.hoveredTile) {
            ctx.font = "20px 'Velvet Dawn'";
            ctx.fillStyle = "#ff0000"
            ctx.fillText(this.hoveredTile.entityId.toString(), sidebarStart, 100)
        }

        if (this.clickedTile) {
            this.buttons.forEach((button, i) => {
                const {x, y} = this.getButtonPosition(i, constants)
                const entity = VelvetDawn.datapacks.entities[button.id];
                let placedUnits: number
                let availableUnits = 1

                if (entity.commander) {
                    placedUnits = setup.placedCommander ? 1 : 0
                } else {
                    placedUnits = setup.units[entity.id] - setup.remainingUnits[entity.id]
                    availableUnits = setup.units[entity.id]
                }

                button
                    .setPos(x, y)
                    .text(`${entity.id} (${placedUnits}/${availableUnits})`)
                    .enabled(placedUnits < availableUnits)
                    .render(ctx, perspective)
            })

            const selectedEntity = VelvetDawn.mapEntities[`${this.clickedTile.x}-${this.clickedTile.y}`]
            if (selectedEntity && selectedEntity.player === VelvetDawn.loginDetails.username) {
                const {x, y} = this.getButtonPosition(this.buttons.length, constants)
                this.removeEntityButton
                    .setPos(x, y)
                    .render(ctx, perspective)
            }
        }

        this.nextTurnButton.enabled(setup.placedCommander).render(ctx, perspective)

        const lineHeight = constants.height - constants.buttonHeight - 2 * constants.sidebarPadding
        ctx.moveTo(constants.sidebarStart + constants.sidebarPadding, lineHeight)
        ctx.lineTo(constants.width - constants.sidebarPadding, lineHeight)
        ctx.stroke()

        this.bannerButton.render(ctx, perspective)

        return undefined;
    }

    onStart(constants: RenderingConstants): null {
        const bannerWidth = 500 * constants.resolution;
        this.bannerButton = new HexButton(bannerWidth, 50 * constants.resolution)
            .setPos(
                (constants.width - constants.sidebar) / 2 - bannerWidth / 2,
                25 * constants.resolution
            )
            .text("Setup Phase")

        this.nextTurnButton = new HexButton(constants.buttonWidth, constants.buttonHeight)
            .setPos(constants.nextTurnButtonStartX, constants.nextTurnButtonStartY)
            .backgroundColor("#66dd00")
            .text("Done");
        this.allButtons.push(this.nextTurnButton);

        this.removeEntityButton = new HexButton(constants.buttonWidth,constants.buttonHeight)
            .backgroundColor("#ff0000")
            .text("Remove Entity")
            .onClick(() => {
                const selectedEntity = VelvetDawn.mapEntities[`${this.clickedTile.x}-${this.clickedTile.y}`]
                if (selectedEntity) {
                    delete VelvetDawn.unitsDict[selectedEntity.id]
                }
                Api.setup.removeEntity(this.clickedTile.x, this.clickedTile.y).then(x => {
                    VelvetDawn.setState(x)
                })
            });
        this.allButtons.push(this.removeEntityButton);

        VelvetDawn.getState().setup.commanders.forEach((key, i) => {
            const commander = VelvetDawn.datapacks.entities[key];

            const button = new IdHexButton(constants.buttonWidth, constants.buttonHeight)
                .icon(commander.textures.background)
                .text(commander.name)
                .textColor("#ffffff")
                .textAlign(TextAlign.Left)
                .backgroundColor("#000000")
                .onClick(() => {
                    Api.setup.placeEntity(key, this.clickedTile.x, this.clickedTile.y).then(x => {
                        VelvetDawn.setState(x)
                    })
                })
            button.id = key

            this.buttons.push(button);
            this.allButtons.push(button);
        })

        Object.keys(VelvetDawn.getState().setup.units).forEach((key, i) => {
            const unit = VelvetDawn.datapacks.entities[key];
            console.log("Creating key " + key)

            const button = new IdHexButton(constants.sidebar - constants.sidebarPadding * 2, constants.buttonHeight)
                .icon(unit.textures.background)
                .text(unit.name)
                .textColor("#ffffff")
                .textAlign(TextAlign.Left)
                .backgroundColor("#000000")
                .onClick(() => {
                    console.log(key)
                    Api.setup.placeEntity(key, this.clickedTile.x, this.clickedTile.y).then(x => {
                        VelvetDawn.setState(x)
                    })
                })
            button.id = key

            this.buttons.push(button);
            this.allButtons.push(button);
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
            this.allButtons.forEach(button => {
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

    private getButtonPosition(index: number, constants: RenderingConstants): Position {
        return {
            x: constants.sidebarStart + constants.sidebarPadding,
            y: index * (constants.buttonHeight + constants.buttonSpacing) + constants.sidebarPadding
        }
    }
}
