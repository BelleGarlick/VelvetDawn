import {Renderable} from "../renderable";


export enum TextAlign {
    Left,
    Center,
    Right
}


export abstract class ButtonBase extends Renderable {

    public x: number = 0
    public y: number = 0

    protected _text: string
    protected _textColor: string = "#ffffff"
    protected _textAlign = TextAlign.Center;

    protected _icon: undefined | string = undefined;

    protected _enabled: boolean = true;

    protected _backgroundColor: string = "#000000"

    private func?: () => void = undefined

    public onClick(func: () => void) {
        this.func = func
        return this
    }

    public performClick() {
        if (this.func && this._enabled)
            this.func()
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

    backgroundColor(color: string) {
        this._backgroundColor = color
        return this;
    }
}
