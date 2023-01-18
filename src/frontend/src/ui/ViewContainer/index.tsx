import * as React from "react";
import {getResourceUrl} from "api/utils";
import {Text} from "ui/Text";


function BackgroundImage() {
    return <div style={{
        position: 'absolute',
        top: '-20px', left: '-20px',
        width: 'calc(100% + 40px)', height: 'calc(100% + 40px)',
        filter: 'blur(8px)',
        backgroundPosition: 'center',
        backgroundSize: 'cover',
        zIndex: '-1',
        backgroundImage: `url(${getResourceUrl('base:textures.ui.background.background.png')})`
    }} />
}


export function ViewContainer({ children }: { children: React.ReactElement | React.ReactElement[] }) {
    return <>
        <BackgroundImage />
        <div style={{
            position: 'absolute',
            top: '0px', left: '0px',
            width: '100%', height: '100%',
            display: 'grid',
            justifyItems: 'center',
            alignItems: 'center',
            gridTemplateRows: '100px auto',
            padding: '20px'
        }}>
            <Text style={{color: 'black', fontSize: '48px', textShadow: ' 0px 0px 5px white'}}>Velvet Dawn</Text>

            <div style={{
                display: 'flex',
                flexDirection: 'column',
                backgroundColor: 'black',
                border: '2px solid white',
                padding: '24px',
                borderRadius: '0px',
                gap: '16px',
                width: '500px',
                maxHeight: 'calc(100vh - 100px)',
                overflow: 'auto',
                margin: '50px'
            }}>
                {children}
            </div>
        </div>
    </>
}