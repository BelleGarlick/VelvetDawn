import * as React from "react";
import {GameState} from "models";


export function LobbyUsers({ state }: { state: GameState }) {
    return <>
        {state.teams.map(team => {
            return <div key={team.id}>
                <span>Team {team.name}</span>
                {team.players.map((player) => {
                    return <div key={player}>{state.players[player].name}</div>
                })}
            </div>
        })}
    </>
}
