import * as React from "react"
import {useEffect, useRef} from "react";
import { Renderer } from "rendering/Renderer";


export function GameView() {
    const canvasRef = useRef(null)

    useEffect(() => {
        Renderer.getInstance()
            .setCanvas(canvasRef.current)
    }, [])

    return <canvas ref={canvasRef} style={{
        width: '100%',
        height: '100%',
        position: 'absolute',
        top: '0px',
        left: '0px'
    }}></canvas>
}
