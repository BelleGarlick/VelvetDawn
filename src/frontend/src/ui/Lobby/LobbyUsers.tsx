import * as React from "react";
import {GameState} from "models";
import { Text } from "../Text"
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";


export function LobbyUsers({ state }: { state: GameState }) {
    return <>
        {state.teams.map(team => {
            return <div key={team.id} style={{
                display: 'flex',
                flexDirection: 'column'
            }}>
                <Text>Team {team.name}</Text>
                {team.players.map((player) => {
                    return <Text key={player}>{VelvetDawn.players[player].name}</Text>
                })}
            </div>
        })}
    </>
}
