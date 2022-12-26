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
    private nextTurnButton: Button = null
    private removeEntityButton: Button = null

    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): undefined {
        const setup = VelvetDawn.getState().setup

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
                    .hovered(button.isHovered(this.mousePosition))
                    .setPos(x, y)
                    .text(`${entity.id} (${placedUnits}/${availableUnits})`)
                    .enabled(placedUnits < availableUnits)
                    .render(ctx, perspective)
            })

            const selectedEntity = VelvetDawn.mapEntities[`${this.clickedTile.x}-${this.clickedTile.y}`]
            if (selectedEntity && selectedEntity.player === VelvetDawn.loginDetails.username) {
                const {x, y} = this.getButtonPosition(this.buttons.length, constants)
                this.removeEntityButton
                    .hovered(this.removeEntityButton.isHovered(this.mousePosition))
                    .setPos(x, y)
                    .render(ctx, perspective)
            }
        }

        const playerReady = VelvetDawn.getState().players[VelvetDawn.loginDetails.username].ready
        this.nextTurnButton
            .hovered(this.nextTurnButton.isHovered(this.mousePosition))
            .setPos(constants.nextTurnButtonStartX, constants.nextTurnButtonStartY)
            .enabled(setup.placedCommander)
            .text(playerReady ? "Unready" : "Ready")
            .backgroundColor(playerReady ? "#33bb00" : "#66dd00")
            .render(ctx, perspective)

        const lineHeight = constants.height - constants.buttonHeight - 2 * constants.sidebarPadding
        ctx.moveTo(constants.sidebarStart + constants.sidebarPadding, lineHeight)
        ctx.lineTo(constants.width - constants.sidebarPadding, lineHeight)
        ctx.stroke()

        this.turnBanner.render(ctx, perspective, constants)

        return undefined;
    }

    onStart(constants: RenderingConstants): null {
        this.turnBanner.title("Setup Phase")

        this.nextTurnButton = new HexButton(constants.buttonWidth, constants.buttonHeight)
            .setPos(constants.nextTurnButtonStartX, constants.nextTurnButtonStartY)
            .backgroundColor("#66dd00")
            .backgroundHoverColor("#99ee33")
            .text("Done")
            .onClick(() => {
                if (VelvetDawn.getState().players[VelvetDawn.loginDetails.username].ready) {
                    Api.turns.unready().then(x => VelvetDawn.setState(x))
                    VelvetDawn.getState().players[VelvetDawn.loginDetails.username].ready = false
                } else {
                    Api.turns.ready().then(x => VelvetDawn.setState(x))
                    VelvetDawn.getState().players[VelvetDawn.loginDetails.username].ready = true
                }

            });
        this.allButtons.push(this.nextTurnButton);

        this.removeEntityButton = new HexButton(constants.buttonWidth,constants.buttonHeight)
            .backgroundColor("#ff0000")
            .backgroundHoverColor("#ff3333")
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

        VelvetDawn.getState().setup.commanders.forEach((key) => {
            const commander = VelvetDawn.datapacks.entities[key];

            const button = new IdHexButton(constants.buttonWidth, constants.buttonHeight)
                .icon(commander.textures.background)
                .text(commander.name)
                .textColor("#ffffff")
                .textAlign(TextAlign.Left)
                .backgroundColor("#000000")
                .backgroundHoverColor("#333333")
                .onClick(() => {
                    Api.setup.placeEntity(key, this.clickedTile.x, this.clickedTile.y).then(x => {
                        VelvetDawn.setState(x)
                    })
                })
            button.id = key

            this.buttons.push(button);
            this.allButtons.push(button);
        })

        Object.keys(VelvetDawn.getState().setup.units).forEach((key) => {
            const unit = VelvetDawn.datapacks.entities[key];
            console.log("Creating key " + key)

            const button = new IdHexButton(constants.sidebar - constants.sidebarPadding * 2, constants.buttonHeight)
                .icon(unit.textures.background)
                .text(unit.name)
                .textColor("#ffffff")
                .textAlign(TextAlign.Left)
                .backgroundColor("#000000")
                .backgroundHoverColor("#333333")
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
                if (button.isHovered({x, y})) {
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
