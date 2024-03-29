import {Renderable} from "../renderable";
import {Position} from "models";
import {VelvetDawn} from "../../../velvet-dawn/velvet-dawn";


export enum TextAlign {
    Left,
    Center,
    Right
}


export abstract class ButtonBase extends Renderable {

    public x: number = 0
    public y: number = 0
    public width: number
    public height: number

    protected _text: string
    protected _textColor: string = "#ffffff"
    protected _textAlign = TextAlign.Center;

    protected _icon: undefined | string = undefined;

    protected _enabled: boolean = true;

    protected _hovered: boolean = false;
    protected _backgroundColor: string = "#000000"
    protected _backgroundHoverColor: string = "#333333"

    private func?: () => void = undefined

    public onClick(func: () => void) {
        this.func = func
        return this
    }

    public performClick() {
        if (this.func && this._enabled) {
            ButtonBase.playAudio()
            this.func()
        }
    }

    text(text: string) {
        this._text = text
        return this
    }

    public enabled(enable: boolean) {
        this._enabled = enable;
        return this;
    }

    textColor(color: string) {
        this._textColor = color
        return this
    }

    textAlign(alignment: TextAlign) {
        this._textAlign = alignment
        return this;
    }

    icon(_icon: string) {
        this._icon = _icon
        return this
    }

    setPos(x: number, y: number) {
        this.x = x
        this.y = y
        return this
    }

    setSize(width: number, height: number) {
        this.width = width
        this.height = height
        return this
    }

    hovered(hovered: boolean) {
        this._hovered = hovered
        return this
    }

    backgroundColor(color: string) {
        this._backgroundColor = color
        return this;
    }

    backgroundHoverColor(color: string) {
        this._backgroundHoverColor = color
        return this;
    }

    isHovered(position: Position | undefined): boolean {
        if (position === undefined)
            return

        const {x, y} = position;
        return x >= this.x
            && x <= this.x + this.width
            && y >= this.y
            && y <= this.y + this.height;
    }

    static playAudio() {
        VelvetDawn.audioPlayers[`base:audio.buttons.button${Math.ceil(Math.random() * 4)}.mp3`].play()
    }
}
