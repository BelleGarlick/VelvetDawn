import {Typography} from "@material-ui/core";
import * as React from "react";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import {GameSetup} from "models/gameSetup";
import * as Api from "api"


function AdminView({ setup, setSetup }: { setup: GameSetup, setSetup: (x: GameSetup) => void }) {

    return <>
        <Typography>Commanders</Typography>
        {Object.keys(VelvetDawn.entities)
            .filter(x => VelvetDawn.entities[x].commander)
            .map(entity => {
            return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={entity}>
                <div>{VelvetDawn.entities[entity].name}</div>
                <div style={{display: 'flex', flexDirection: 'row'}}>
                    {!setup.commanders.includes(entity) && <button onClick={() => {
                        Api.setup.updateGameSetup(entity, 1).then(setSetup)
                    }}>Add</button>}
                    {setup.commanders.includes(entity) && <button onClick={() => {
                        Api.setup.updateGameSetup(entity, 0).then(setSetup)
                    }}>Remove</button>}
                </div>
            </div>
        })}

        <Typography>Units</Typography>
        {Object.keys(VelvetDawn.entities)
            .filter(x => !VelvetDawn.entities[x].commander)
            .map(entity => {
            return <div style={{
                display: 'flex',
                justifyContent: 'space-between'
            }} key={entity}>
                <div>{VelvetDawn.entities[entity].name}</div>
                <div style={{display: 'flex', flexDirection: 'row'}}>
                    <button onClick={() => {
                        console.log(setup.units[entity])
                        Api.setup.updateGameSetup(entity, (setup.units[entity] ?? 0) - 1).then(setSetup)
                    }}>-</button>
                    <div>{setup.units[entity]}</div>
                    <button onClick={() => {
                        Api.setup.updateGameSetup(entity, (setup.units[entity] ?? 0) + 1).then(setSetup)
                    }}>+</button>
                </div>
            </div>
        })}
    </>
}


function NonAdminView({ setup }: { setup: GameSetup }) {
    return <>
        <Typography>Commanders</Typography>
        <div>
            {setup.commanders.map((commander) => {
                return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={commander}>
                    <div>{VelvetDawn.entities[commander].name}</div>
                    <div><button>i</button></div>
                </div>
            })}
        </div>

        <Typography>Units</Typography>
        <div>
            {Object.keys(setup.units).map((unit) => {
                return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={unit}>
                    <p>{VelvetDawn.entities[unit].name}</p>
                    <div style={{ display: 'flex', flexDirection: 'row' }}>
                        <div>{setup.units[unit]}</div>
                        <div><button>i</button></div>
                    </div>
                </div>
            })}
        </div>
    </>
}


export function LobbyUnits({ setup, setSetup }: { setup?: GameSetup, setSetup: (x: GameSetup) => void }) {
    const userIsAdmin = VelvetDawn.getPlayer()?.admin == true

    if (!setup)
        return <></>

    return <>
        {userIsAdmin && <AdminView setup={setup!} setSetup={setSetup} />}
        {!userIsAdmin && <NonAdminView setup={setup!} />}
    </>
}
