import * as React from "react";
import {GameState} from "models";
import { Text } from "../Text"


export function LobbyUsers({ state }: { state: GameState }) {
    return <>
        {state.teams.map(team => {
            return <div key={team.id} style={{
                display: 'flex',
                flexDirection: 'column'
            }}>
                <Text>Team {team.name}</Text>
                {team.players.map((player) => {
                    return <Text key={player}>{state.players[player].name}</Text>
                })}
            </div>
        })}
    </>
}
