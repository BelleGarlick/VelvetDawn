import {Position} from "models";


export function normalise(position: Position) {
    const l = length(position)
    if (l === 0)
        return {x: 0, y: 0}
    return {
        x: position.x / l,
        y: position.y / l
    }
}


export function length(position: Position) {
    return Math.hypot(position.y, position.x)
}


export function sub(a: Position, b: Position) {
    return {
        x: a.x - b.x,
        y: a.y - b.y
    }
}


export function add(a: Position, b: Position) {
    return {
        x: a.x + b.x,
        y: a.y + b.y
    }
}


export function multiply(a: Position, b: number) {
    return {
        x: a.x * b,
        y: a.y * b
    }
}
