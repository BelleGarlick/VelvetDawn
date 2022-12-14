import * as React from "react";
import {getUrl} from "api/utils";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {MENU_AUDIO_ID} from "../../constants";


export function InitialResourceLoadingScreen({ children }: { children: React.ReactElement }) {
    const [loading, setLoading] = React.useState(true);

    React.useEffect(() => {
        VelvetDawn.audioPlayers["velvet-dawn:menu.mp3"] = new Audio(`${getUrl()}resources/${MENU_AUDIO_ID}/`)
        new FontFace('Velvet Dawn', `url(${getUrl()}resources/velvet-dawn:font.woff)`).load().then((loaded_face) => {
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
