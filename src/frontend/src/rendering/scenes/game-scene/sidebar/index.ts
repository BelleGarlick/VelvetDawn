import {NextTurnButton} from "../../../entities/buttons/next-turn-button";
import {TabButtons} from "../../../entities/buttons/tabs";
import {RenderingConstants} from "../../scene";
import {RenderingFacade} from "../../../facade";
import {Line} from "../../../entities/line";
import {UnitEntity} from "../../../entities/unit-entity";
import {Textures} from "../../../Textures";
import {VelvetDawn} from "../../../../velvet-dawn/velvet-dawn";
import {Rectangle} from "../../../entities/rectangle";


/** Game View sidebar
 *
 * This class renders all aspects of the sidebar UI in game. This
 * includes attributes, actions and upgrades of the UI.
 *
 */


export class GameViewSidebar {

    private sidebarBackground: Rectangle = null

    public selectedEntity: UnitEntity | undefined = undefined
    private topLine = new Line()
    private attributesLine = new Line()

    private unitTabs: TabButtons;
    private tab: number = 0;

    nextTurnButton: NextTurnButton = null

    constructor(constants: RenderingConstants) {
        this.sidebarBackground = new Rectangle()
        this.nextTurnButton = new NextTurnButton(constants);
        this.unitTabs = new TabButtons(
            ["Abilities", "Upgrades", "Info"],
            (tab) => this.tab = tab
        );
    }

    /** Render the whole sidebar */
    render(facade: RenderingFacade) {
        this.sidebarBackground
            .setFrame(facade.constants.sidebarStart, 0, facade.constants.sidebar, facade.constants.height)
            .render(facade)

        if (this.selectedEntity) {
            let remainingTop = this.renderUnitBanner(facade)
            remainingTop = this.renderUnitAttributes(facade, remainingTop)

            this.attributesLine.setLine({ x: facade.sidebarInnerStart, y: remainingTop }, {
                x: facade.constants.width - facade.constants.sidebarPadding,
                y: remainingTop
            }).render(facade)

            this.unitTabs.setMousePos(facade.mousePosition).setPosition({
                x: facade.constants.sidebarStart + facade.constants.sidebarPadding,
                y: remainingTop + facade.constants.sidebarPadding
            }).render(facade)
        }

        this.nextTurnButton.draw(facade)
    }

    /** Render the unit banner
     *
     * This shows the unit name and image
     *
     * @param facade
     * @returns Y position where the next component should render from
     */
    renderUnitBanner(facade: RenderingFacade): number {
        const { ctx, sidebarInnerStart } = facade;

        const unit = VelvetDawn.datapacks.entities[this.selectedEntity.entityId]
        const texture = Textures.get(unit.textures.background)
        const size = facade.constants.buttonHeight;

        ctx.drawImage(
            texture,
            0, 0,
            texture.width, texture.height,
            sidebarInnerStart, facade.constants.sidebarPadding,
            size, size
        )

        ctx.fillStyle = "#ffffff"
        ctx.textBaseline = "middle"
        ctx.font = "50px 'Velvet Dawn'";
        ctx.textAlign = "left"
        ctx.fillText(unit.name, sidebarInnerStart + size + facade.constants.sidebarPadding, facade.constants.sidebarPadding + size / 2)
        ctx.fill()

        this.topLine.setLine(
            {x: facade.sidebarInnerStart, y: facade.constants.sidebarPadding * 2 + facade.constants.buttonHeight},
            {x: facade.constants.width - facade.constants.sidebarPadding, y: facade.constants.sidebarPadding * 2 + facade.constants.buttonHeight},
        ).render(facade)

        return facade.constants.sidebarPadding * 3 + facade.constants.buttonHeight
    }

    /** Render the unit attributes
     *
     * @param facade
     * @param top The Y pos to render the attributes from
     * @returns Y position where the next component should render from
     */
    renderUnitAttributes(facade: RenderingFacade, top: number): number {
        const { ctx } = facade;

        const sidebarInnerLeft = facade.constants.sidebarStart + facade.constants.sidebarPadding
        const attributeCols = 3

        const unit = VelvetDawn.datapacks.entities[this.selectedEntity.entityId]
        const attributes = unit.attributes.filter(x => x.icon !== null)

        const attributeWidth = (facade.constants.sidebar - 2 * facade.constants.sidebarPadding) / attributeCols
        const size = facade.constants.buttonHeight / 2;

        // Iterate through each attribute to render it within the number of defined columns
        attributes.forEach((attribute, i) => {
            const x = sidebarInnerLeft + attributeWidth * (i % attributeCols)
            const y = top + ((size + facade.constants.sidebarPadding) * Math.floor(i / attributeCols))

            const texture = Textures.get(attribute.icon)
            ctx.drawImage(
                texture,
                0, 0,
                texture.width, texture.height,
                x, y, size, size
            )

            ctx.fillStyle = "#ffffff"
            ctx.font = "35px 'Velvet Dawn'";
            ctx.fillText(this.selectedEntity.attributes[attribute.id], x + size + facade.constants.sidebarPadding, y + size / 2)
            ctx.fill()
        })

        return top + (Math.ceil(attributes.length / 3) * (size + facade.constants.sidebarPadding))
    }

    /** Called when the user clicks within the sidebar
     *
     * @param position Where the user clicked
     */
    clicked(position: { x: number; y: number }) {
        [this.nextTurnButton].forEach(button => {
            if (button.isHovered(position))
                button.performClick()
        })
        this.unitTabs.click()
    }
}
