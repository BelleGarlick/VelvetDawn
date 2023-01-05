import {HexButton} from "./hex-button";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import * as Api from "api";
import {RenderingConstants} from "../../scenes/scene";
import {RenderingFacade} from "../../facade";


export class NextTurnButton extends HexButton {
    constructor(constants: RenderingConstants) {
        super(constants.buttonWidth, constants.buttonHeight)

        this
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
    }

    draw(facade: RenderingFacade) {
        const playerReady = VelvetDawn.getState().players[VelvetDawn.loginDetails.username].ready

        const placedCommander = VelvetDawn.getState().setup.placedCommander
        let buttonText = playerReady ? "Unready" : "Ready"
        if (!placedCommander)
            buttonText = "Place a Commander"

        this
            .hovered(this.isHovered(facade.mousePosition))
            .setPos(facade.constants.nextTurnButtonStartX, facade.constants.nextTurnButtonStartY)
            .enabled(placedCommander)
            .text(buttonText)
            .backgroundColor(playerReady ? "#33bb00" : "#66dd00")
            .render(facade)
    }
}
