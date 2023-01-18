import * as React from "react";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import * as Api from "api"
import {LobbyUsers} from "./LobbyUsers";
import {LobbyUnits} from "./LobbyUnits";
import {GameSetup, ViewState} from "models";
import {Renderer} from "../../rendering/Renderer";
import { Button } from "ui/Button";
import { Text } from "ui/Text";


let time: any = -1


export function Lobby({ setView }: { setView: (x: ViewState) => void }) {
    const userIsAdmin = VelvetDawn.getPlayer()?.admin === true

    const [tab, setTab] = React.useState(0);
    const [state, setGameState] = React.useState(VelvetDawn.getState);
    const [gameSetup, setGameSetup] = React.useState<GameSetup>(null);

    React.useEffect(() => {
        time = setInterval(() => {
            setGameState(VelvetDawn.getState)
            setGameSetup(VelvetDawn.getState().setup)

            if (VelvetDawn.getState().phase !== "lobby") {
                setView(ViewState.Game)

                Renderer.startScene()
                clearInterval(time)
            }
        }, 1000)

        return () => {
            clearInterval(time)
        };
    }, []);

    return <>
        <div style={{
            display: 'flex',
            flexDirection: 'row'
        }}>
            <Button onClick={() => setTab(0)}>Players</Button>
            <Button onClick={() => setTab(1)}>Units</Button>
        </div>
        {tab === 0 && <LobbyUsers state={state} />}
        {tab === 1 && <LobbyUnits setup={gameSetup} setSetup={setGameSetup} />}

        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
        }}>
            {userIsAdmin && (<>
                <Button onClick={() => {
                    Api.setup.startSetup().then(x => {
                        VelvetDawn.setState(x)
                    })
                }}>Start</Button>
                <Button onClick={() => {
                    setView(ViewState.DatapackEditor)
                }}>Datapack Editor</Button>
            </>)}
        </div>
    </>
}
