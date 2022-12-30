import * as React from "react";
import {getResourceUrl} from "api/utils";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {FONT_ID, MENU_AUDIO_ID} from "../../constants";


export function InitialResourceLoadingScreen({ children }: { children: React.ReactElement }): JSX.Element {
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        VelvetDawn.audioPlayers[MENU_AUDIO_ID] = new Audio(getResourceUrl(MENU_AUDIO_ID))
        const fontUrl = getResourceUrl(FONT_ID);
        console.log(fontUrl)
        new FontFace('Velvet Dawn', `url(${fontUrl})`).load().then((loaded_face) => {
            // @ts-ignore
            document.fonts.add(loaded_face);
            setLoading(false)
        }).catch((error) => {
            alert("Unable to load fonts. Please reload")
            console.error(error);
        });
    }, [])

    if (loading)
        return <div>Loading</div>

    return children
}
