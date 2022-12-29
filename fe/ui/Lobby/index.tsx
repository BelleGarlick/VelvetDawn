import * as React from "react";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {Typography} from "@material-ui/core";
import * as Api from "api"
import {LobbyUsers} from "ui/Lobby/LobbyUsers";
import {LobbyUnits} from "ui/Lobby/LobbyUnits";
import {ViewState, GameSetup} from "models";
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

                Renderer.getInstance().getScene().onStart(Renderer.getConstants())
                clearInterval(time)
            }
        }, 1000)

        return () => {
            clearInterval(time)
        };
    }, []);

    return <>
        <Typography>Welcome {VelvetDawn.loginDetails.username}</Typography>
        <div style={{
            display: 'flex',
            flexDirection: 'row'
        }}>
            <button onClick={() => setTab(0)}>Players</button>
            <button onClick={() => setTab(1)}>Units</button>
        </div>
        {tab === 0 && <LobbyUsers state={state} />}
        {tab === 1 && <LobbyUnits setup={gameSetup} setSetup={setGameSetup} />}

        {userIsAdmin && <button onClick={() => {
            Api.setup.startSetup().then(x => {
                VelvetDawn.setState(x)
            })
        }}>Start</button>}
    </>
}
