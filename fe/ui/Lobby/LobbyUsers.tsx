import {Typography} from "@material-ui/core";
import * as React from "react";
import {GameState} from "models";


export function LobbyUsers({ state }: { state: GameState }) {
    return <>
        {state.teams.map(team => {
            return <div key={team.id}>
                <Typography>Team {team.name}</Typography>
                {team.players.map((player) => {
                    return <div key={player}>{state.players[player].name}</div>
                })}
            </div>
        })}
    </>
}
