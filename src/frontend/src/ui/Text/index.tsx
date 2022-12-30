import * as React from "react";

export function Text({children}: {children: string}) {
    return <span style={{ fontFamily: "'Velvet Dawn', sans-serif" }}>{children}</span>
}
