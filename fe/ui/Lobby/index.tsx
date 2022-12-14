import * as React from "react";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {Typography} from "@material-ui/core";


export function Lobby() {
    const [state, setGameState] = React.useState(VelvetDawn.state);
    const [time, setTimer] = React.useState<any>(-1)

    React.useEffect(() => {
        setTimer(setInterval(() => {
            setGameState(VelvetDawn.state)
        }, 1000))

        return () => {
            clearInterval(time)
        };
    }, []);

    return <>
        <Typography>{VelvetDawn.loginDetails.username}</Typography>
        <hr />
        <div>Players List</div>
        {state.teams.map(team => {
            return <>
                <Typography>Team {team.name}</Typography>
                {team.players.map((player) => {
                    return <div>{player.name}</div>
                })}
            </>
        })}
    </>
}
