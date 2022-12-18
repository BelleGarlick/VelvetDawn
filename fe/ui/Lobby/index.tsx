import * as React from "react";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {Typography} from "@material-ui/core";
import * as Api from "api"
import {GameSetup} from "models/gameSetup";
import {LobbyUsers} from "ui/Lobby/LobbyUsers";
import {LobbyUnits} from "ui/Lobby/LobbyUnits";
import {ViewState} from "models/view-state";


export function Lobby({ setView }: { setView: (x: ViewState) => void }) {
    const userIsAdmin = VelvetDawn.getPlayer()?.admin == true

    const [tab, setTab] = React.useState(0);
    const [state, setGameState] = React.useState(VelvetDawn.state);
    const [gameSetup, setGameSetup] = React.useState<GameSetup>(null);
    const [time, setTimer] = React.useState<any>(-1)

    React.useEffect(() => {
        setTimer(setInterval(() => {
            setGameState(VelvetDawn.state)
            Api.setup.getEntitySetup().then(setGameSetup)

            if (VelvetDawn.state.phase != "lobby") {
                setView(ViewState.Game)
            }
        }, 1000))

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
        {tab == 0 && <LobbyUsers state={state} />}
        {tab == 1 && <LobbyUnits setup={gameSetup} setSetup={setGameSetup} />}

        {userIsAdmin && <button onClick={() => {
            Api.setup.startSetup().then(x => {
                VelvetDawn.state = x
            })
        }}>Start</button>}
    </>
}
