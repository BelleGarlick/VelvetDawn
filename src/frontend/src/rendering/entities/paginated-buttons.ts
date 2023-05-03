import {ActionButton} from "../scenes/game-scene/sidebar/actionButton";
import {RenderingFacade} from "../facade";


export class PaginatedButtons {

    tabPage: number = 0

    resetTabPage() {
        this.tabPage = 0
    }

    render(facade: RenderingFacade, buttons: ActionButton[], startY: number) {
        const pixelsHeight = facade.height - startY - facade.constants.sidebarPadding * 3 - facade.constants.buttonHeight
        let buttonsPerPage = Math.floor(pixelsHeight / (facade.constants.buttonHeight + facade.constants.sidebarPadding))
        buttonsPerPage = 100 // Remove this when fully implementing
        buttons.forEach((button, i) => {
            if (i < buttonsPerPage) {
                button
                    .setPos(facade.sidebarInnerStart, startY + i * (facade.constants.buttonHeight + facade.constants.sidebarPadding))
                    .setSize(facade.constants.sidebar - 2 * facade.constants.sidebarPadding, facade.constants.buttonHeight)
                    .hovered(button.isHovered(facade.mousePosition))
                    .render(facade)
            } else {
                button.hovered(false)
            }
        })
    }
}
