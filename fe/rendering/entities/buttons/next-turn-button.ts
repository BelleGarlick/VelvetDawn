import {HexButton} from "./hex-button";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";
import * as Api from "api/index";
import {RenderingConstants} from "../../scenes/scene";
import {Perspective} from "../../perspective";
import {Position} from "models/position";


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


    draw(ctx: CanvasRenderingContext2D, perspective: Perspective, constants: RenderingConstants, mousePosition: Position) {
        const playerReady = VelvetDawn.getState().players[VelvetDawn.loginDetails.username].ready

        this
            .hovered(this.isHovered(mousePosition))
            .setPos(constants.nextTurnButtonStartX, constants.nextTurnButtonStartY)
            .enabled(VelvetDawn.getState().setup.placedCommander)
            .text(playerReady ? "Unready" : "Ready")
            .backgroundColor(playerReady ? "#33bb00" : "#66dd00")
            .render(ctx, perspective)
    }
}
