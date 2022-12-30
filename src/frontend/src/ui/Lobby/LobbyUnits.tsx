import * as React from "react";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import * as Api from "api"
import {GameSetup} from "models";


function AdminView({ setup, setSetup }: { setup: GameSetup, setSetup: (x: GameSetup) => void }) {
    return <>
        <span>Commanders</span>
        {Object.keys(VelvetDawn.datapacks.entities)
            .filter(x => VelvetDawn.datapacks.entities[x].commander)
            .map(entity => {
            return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={entity}>
                <div>{VelvetDawn.datapacks.entities[entity].name}</div>
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

        <span>Units</span>
        {Object.keys(VelvetDawn.datapacks.entities)
            .filter(x => !VelvetDawn.datapacks.entities[x].commander)
            .map(entity => {
            return <div style={{
                display: 'flex',
                justifyContent: 'space-between'
            }} key={entity}>
                <div>{VelvetDawn.datapacks.entities[entity].name}</div>
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
        <span>Commanders</span>
        <div>
            {setup.commanders.map((commander) => {
                return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={commander}>
                    <div>{VelvetDawn.datapacks.entities[commander].name}</div>
                    <div><button>i</button></div>
                </div>
            })}
        </div>

        <span>Units</span>
        <div>
            {Object.keys(setup.units).map((unit) => {
                return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={unit}>
                    <p>{VelvetDawn.datapacks.entities[unit].name}</p>
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
    const userIsAdmin = VelvetDawn.getPlayer()?.admin === true

    if (!setup)
        return <></>

    return <>
        {userIsAdmin && <AdminView setup={setup!} setSetup={setSetup} />}
        {!userIsAdmin && <NonAdminView setup={setup!} />}
    </>
}
