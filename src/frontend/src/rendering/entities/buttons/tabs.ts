import {Renderable} from "../renderable";
import {Position} from "models/position";
import {ButtonBase} from "./button-base";
import {RenderingFacade} from "../../facade";

export class TabButtons extends Renderable {

    private readonly tabs: string[];
    private selected = 0
    private readonly onChange: (tab: number) => void;

    private mousePos: Position = {x: 0, y: 0}
    private mouseInTab: number = -1

    private position: Position = {x: 0, y: 0}

    constructor(tabs: string[], onChange: (tab: number) => void) {
        super();
        this.tabs = tabs
        this.onChange = onChange
    }

    render(facade: RenderingFacade): null {
        const height = facade.constants.tabHeight;
        const tabWidth = (facade.constants.sidebar - 2 * facade.constants.sidebarPadding) / this.tabs.length

        const hexpoints = facade.perspective.computeHexPoints(facade.constants.sidebar - 2 * facade.constants.sidebarPadding, facade.constants.tabHeight)

        this.mouseInTab = -1
        this.tabs.forEach((tab, i) => {
            facade.ctx.beginPath()
            const x = this.position.x + tabWidth * i

            facade.ctx.fillStyle = this.selected === i
                ? "#333333"
                : "#000000"
            if (this.mousePos.x >= x
                && this.mousePos.x <= x + tabWidth
                && this.mousePos.y >= this.position.y
                && this.mousePos.y <= this.position.y + height) {
                facade.ctx.fillStyle = "#666666"
                this.mouseInTab = i
            }

            facade.ctx.strokeStyle = "#ffffff"
            facade.ctx.lineWidth = 3
            if (i === 0) {
                facade.ctx.moveTo(x + tabWidth, this.position.y)
                facade.ctx.lineTo(x + tabWidth, this.position.y + hexpoints[2].y)
                facade.ctx.lineTo(x + hexpoints[2].x, this.position.y + hexpoints[2].y)
                facade.ctx.lineTo(x + hexpoints[3].x, this.position.y + hexpoints[3].y)
                facade.ctx.lineTo(x + hexpoints[4].x, this.position.y + hexpoints[4].y)
                facade.ctx.lineTo(x + tabWidth, this.position.y)
            } else if (i === this.tabs.length - 1) {
                facade.ctx.moveTo(x, this.position.y)
                facade.ctx.lineTo(this.position.x + hexpoints[5].x, this.position.y + hexpoints[5].y)
                facade.ctx.lineTo(this.position.x + hexpoints[0].x, this.position.y + hexpoints[0].y)
                facade.ctx.lineTo(this.position.x + hexpoints[1].x, this.position.y + hexpoints[1].y)
                facade.ctx.lineTo(x, this.position.y + hexpoints[2].y)
                facade.ctx.lineTo(x, this.position.y)
            } else {
                facade.ctx.rect(x, this.position.y, tabWidth, height)
            }
            facade.ctx.stroke()
            facade.ctx.fill()

            facade.ctx.font = "30px 'Velvet Dawn'";
            facade.ctx.fillStyle = "#ffffff"
            facade.ctx.textBaseline = "middle"
            facade.ctx.textAlign = "center"
            facade.ctx.fillText(this.tabs[i], x + tabWidth / 2, this.position.y + height / 2)
        })

        return null;
    }

    setMousePos(mousePosition: Position) {
        if (mousePosition !== undefined)
            this.mousePos = mousePosition
        return this
    }

    click() {
        if (this.mouseInTab >= 0 && this.mouseInTab < this.tabs.length) {
            this.setTab(this.mouseInTab)
        }
    }

    setPosition(position: Position) {
        this.position = position
        return this
    }

    setTab(tab: number) {
        this.onChange(tab)
        this.selected = tab
        ButtonBase.playAudio();
    }
}
