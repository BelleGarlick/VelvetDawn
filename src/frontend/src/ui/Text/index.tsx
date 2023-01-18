import * as React from "react";

export function Text({children, color, size, style}: {children: React.ReactNode, size?: number, color?: string, style?: React.CSSProperties}) {
    return <span style={{
        fontFamily: "'Velvet Dawn', sans-serif",
        color: 'white',
        ...(style ?? {})
    }}>{children}</span>
}
