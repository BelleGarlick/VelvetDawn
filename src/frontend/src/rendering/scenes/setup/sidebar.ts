import {Renderable} from "../../entities/renderable";
import {RenderingFacade} from "../../facade";
import {NextTurnButton} from "../../entities/buttons/next-turn-button";
import {TabButtons} from "../../entities/buttons/tabs";
import {Button, HexButton, TextAlign} from "../../entities/buttons";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import * as Api from "api/index";
import {RenderingConstants} from "../scene";
import {Position} from "models/position";
import {TileEntity} from "../../entities/tile-entity";


class IdHexButton extends HexButton {
    public id: string = null
}


export class SetupSceneSidebar extends Renderable {

    public clickedTile: TileEntity

    private tabView: number = 0
    public tabButtons: TabButtons

    private commanderButtons: IdHexButton[] = []
    private unitButtons: IdHexButton[] = []
    public removeEntityButton: Button = null

    public nextTurnButton: NextTurnButton = null


    constructor(facade: RenderingFacade) {
        super();
        const { constants } = facade;

        this.tabButtons = new TabButtons(["Commanders", "Units"], (tab) => this.tabView = tab)
        this.nextTurnButton = new NextTurnButton(facade.constants);

        this.removeEntityButton = new HexButton(constants.buttonWidth,constants.buttonHeight)
            .backgroundColor("#ff0000")
            .backgroundHoverColor("#ff3333")
            .text("Remove Entity")
            .onClick(() => VelvetDawn.map.removeEntityDuringSetup(this.clickedTile.position));

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
                    Api.setup.placeEntity(key, this.clickedTile.position).then(x => {
                        VelvetDawn.setState(x)
                    })
                })
            button.id = key

            this.commanderButtons.push(button);
        })

        Object.keys(VelvetDawn.getState().setup.entities).forEach((key) => {
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
                    Api.setup.placeEntity(key, this.clickedTile.position).then(x => {
                        VelvetDawn.setState(x)
                    })
                })
            button.id = key

            this.unitButtons.push(button);
        })
    }

    render(facade: RenderingFacade): null {
        facade.ctx.fillStyle = "#000000"
        facade.ctx.fillRect(facade.constants.sidebarStart, 0, facade.constants.sidebar, facade.constants.height)

        const setup = VelvetDawn.getState().setup

        this.tabButtons
            .setPosition({x: facade.sidebarInnerStart, y: facade.constants.sidebarPadding})
            .setMousePos(facade.mousePosition)
            .render(facade)

        this.nextTurnButton.draw(facade)

        const buttons = this.getVisibleButtons()

        if (this.clickedTile) {
            buttons.forEach((button, i) => {
                const {x, y} = this.getButtonPosition(i, facade.constants)
                const entity = VelvetDawn.datapacks.entities[button.id];
                let placedUnits: number
                let availableUnits = 1

                if (entity.commander) {
                    placedUnits = setup.placedCommander ? 1 : 0
                } else {
                    placedUnits = setup.entities[entity.datapackId] - setup.remainingEntities[entity.datapackId]
                    availableUnits = setup.entities[entity.datapackId]
                }

                button
                    .hovered(button.isHovered(facade.mousePosition))
                    .setPos(x, y)
                    .text(`${entity.name} (${placedUnits}/${availableUnits})`)
                    .enabled(placedUnits < availableUnits)
                    .render(facade)
            })

            const selectedEntities = VelvetDawn.map.getUnitsAtPosition(this.clickedTile.position)
            selectedEntities.forEach(selectedEntity => {
                if (selectedEntity.player === VelvetDawn.loginDetails.username) {
                    const {x, y} = this.getButtonPosition(buttons.length, facade.constants)
                    this.removeEntityButton
                        .hovered(this.removeEntityButton.isHovered(facade.mousePosition))
                        .setPos(x, y)
                        .render(facade)
                }
            })
        }

        let topLineHeight = facade.constants.tabHeight + 2 * facade.constants.sidebarPadding
        facade.ctx.moveTo(facade.sidebarStart + facade.sidebarPadding, topLineHeight)
        facade.ctx.lineTo(facade.constants.width - facade.sidebarPadding, topLineHeight)
        facade.ctx.stroke()

        const lineHeight = facade.constants.height - facade.constants.buttonHeight - 2 * facade.constants.sidebarPadding
        facade.ctx.moveTo(facade.constants.sidebarStart + facade.constants.sidebarPadding, lineHeight)
        facade.ctx.lineTo(facade.constants.width - facade.constants.sidebarPadding, lineHeight)
        facade.ctx.stroke()

        return null;
    }

    public toggleTab() {
        this.tabButtons.setTab(1 - this.tabView)
    }

    public getVisibleButtons() {
        return this.tabView === 0
            ? this.commanderButtons
            : this.unitButtons;
    }

    private getButtonPosition(index: number, constants: RenderingConstants): Position {
        return {
            x: constants.sidebarStart + constants.sidebarPadding,
            y: index * (constants.buttonHeight + constants.buttonSpacing) + constants.sidebarPadding * 2 + constants.tabHeight + constants.buttonSpacing
        }
    }
}
