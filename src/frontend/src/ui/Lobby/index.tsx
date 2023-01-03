import * as React from "react";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import * as Api from "api"
import {LobbyUsers} from "./LobbyUsers";
import {LobbyUnits} from "./LobbyUnits";
import {GameSetup, ViewState} from "models";
import {Renderer} from "../../rendering/Renderer";


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
        <span>Welcome {VelvetDawn.loginDetails.username}</span>
        <div style={{
            display: 'flex',
            flexDirection: 'row'
        }}>
            <button onClick={() => setTab(0)}>Players</button>
            <button onClick={() => setTab(1)}>Units</button>
        </div>
        {tab === 0 && <LobbyUsers state={state} />}
        {tab === 1 && <LobbyUnits setup={gameSetup} setSetup={setGameSetup} />}

        {userIsAdmin && (<>
            <button onClick={() => {
                Api.setup.startSetup().then(x => {
                    VelvetDawn.setState(x)
                })
            }}>Start</button>
            <button onClick={() => {
                setView(ViewState.DatapackEditor)
            }}>Datapack Editor</button>
        </>)}
    </>
}
