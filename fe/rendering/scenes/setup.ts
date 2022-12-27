import {RenderingConstants, Scene} from "./scene";
import {Perspective} from "../perspective";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import * as Api from 'api'
import {Button, HexButton, TextAlign} from "../entities/buttons"
import {Position} from "models/position";
import {NextTurnButton} from "../entities/buttons/next-turn-button";


class IdHexButton extends HexButton {
    public id: string = null
}


export class SetupPhase extends Scene {

    private tabView: number = 0

    private commanderButtons: IdHexButton[] = []
    private unitButtons: IdHexButton[] = []
    private commanderTab: Button = null
    private unitsTab: Button = null
    private removeEntityButton: Button = null
    private nextTurnButton: NextTurnButton = null

    render(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants): undefined {
        const setup = VelvetDawn.getState().setup

        const buttons = this.getVisibleButtons()

        if (this.clickedTile) {
            buttons.forEach((button, i) => {
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
                const {x, y} = this.getButtonPosition(buttons.length, constants)
                this.removeEntityButton
                    .hovered(this.removeEntityButton.isHovered(this.mousePosition))
                    .setPos(x, y)
                    .render(ctx, perspective)
            }
        }


        let topLineHeight = constants.buttonHeight + 2 * constants.sidebarPadding
        ctx.moveTo(constants.sidebarStart + constants.sidebarPadding, topLineHeight)
        ctx.lineTo(constants.width - constants.sidebarPadding, topLineHeight)
        ctx.stroke()

        const lineHeight = constants.height - constants.buttonHeight - 2 * constants.sidebarPadding
        ctx.moveTo(constants.sidebarStart + constants.sidebarPadding, lineHeight)
        ctx.lineTo(constants.width - constants.sidebarPadding, lineHeight)
        ctx.stroke()

        this.commanderTab
            .hovered(this.commanderTab.isHovered(this.mousePosition))
            .setPos(constants.sidebarStart + constants.sidebarPadding, constants.sidebarPadding)
            .render(ctx, perspective)
        this.unitsTab
            .hovered(this.unitsTab.isHovered(this.mousePosition))
            .setPos(constants.sidebarStart + 2 * constants.sidebarPadding + this.unitsTab.width, constants.sidebarPadding)
            .render(ctx, perspective)

        this.nextTurnButton.draw(ctx, perspective, constants, this.mousePosition)
        this.turnBanner.render(ctx, perspective, constants)

        return undefined;
    }

    onStart(constants: RenderingConstants): null {
        this.turnBanner.title("Setup Phase")
        this.nextTurnButton = new NextTurnButton(constants);

        if (VelvetDawn.map.length > 0 && VelvetDawn.getState().spawnArea.length > 0) {
            VelvetDawn.getState().spawnArea.forEach(({x, y}) => {
                VelvetDawn.map[x][y].isSpawnArea = true
            })
        }

        const tabWidth = (constants.sidebar - 3 * constants.sidebarPadding) / 2
        this.commanderTab = new HexButton(tabWidth, constants.buttonHeight)
            .text("Commanders")
            .onClick(() => this.tabView = 0)

        this.unitsTab = new HexButton(tabWidth, constants.buttonHeight)
            .text("Units")
            .onClick(() => this.tabView = 1)

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

            this.commanderButtons.push(button);
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

            this.unitButtons.push(button);
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
            [
                ...this.getVisibleButtons(),
                this.commanderTab,
                this.unitsTab,
                this.nextTurnButton,
                this.removeEntityButton
            ].forEach(button => {
                if (button.isHovered({x, y}))
                    button.performClick()
            })
        }

        return null
    }

    keyboardInput(event: KeyboardEvent): null {
        // Switch tab
        if (event.key === "Tab") {
            this.tabView = 1 - this.tabView;
            event.preventDefault();
        }

        // Place item
        if (event.keyCode >= 49 && event.keyCode <= 57) {
            const buttonIndex = event.keyCode - 49;
            const buttons = this.getVisibleButtons()
            if (buttonIndex < buttons.length)
                buttons[buttonIndex].performClick()
            event.preventDefault()
        }

        // Remove Item
        if (event.key === "Backspace") {
            this.removeEntityButton.performClick();
            event.preventDefault()
        }

        // Ready up
        if (event.key === "Enter") {
            this.nextTurnButton.performClick();
            event.preventDefault()
        }

        return null
    }

    getVisibleButtons() {
        return this.tabView === 0
            ? this.commanderButtons
            : this.unitButtons;
    }

    private getButtonPosition(index: number, constants: RenderingConstants): Position {
        return {
            x: constants.sidebarStart + constants.sidebarPadding,
            y: (index + 1) * (constants.buttonHeight + constants.buttonSpacing) + constants.sidebarPadding * 2
        }
    }
}
