import * as React from "react";

export function Button({children, onClick, style}: {children: string, onClick: () => void, style?: React.CSSProperties}) {
    const [hovered, setHovered] = React.useState(false);
    const [clicked, setClicked] = React.useState(false);

    return <button
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => {
            setClicked(false)
            setHovered(false)
        }}
        onMouseDown={() => setClicked(true)}
        onMouseUp={() => setClicked(false)}
        onClick={onClick}
        style={{
            width: 'fit-content',
            background: clicked ?  '#444444' : (hovered ? '#222222' : 'black'),
            border: '0px solid white',
            borderRadius: '0px',
            fontFamily: "'Velvet Dawn', sans-serif",
            fontSize: '18px',
            color: 'white',
            padding: '8px 20px',
            ...(style ?? {})
        }}>
        {children}
    </button>
}
