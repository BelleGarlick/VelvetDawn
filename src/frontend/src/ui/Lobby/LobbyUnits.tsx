import * as React from "react";
import {VelvetDawn} from "../../velvet-dawn/velvet-dawn";
import * as Api from "api"
import {GameSetup} from "models";
import { Button } from "ui/Button";
import { Text } from "ui/Text";


const ButtonPadding = '5px 10px'


function AdminView({ setup, setSetup }: { setup: GameSetup, setSetup: (x: GameSetup) => void }) {
    return <>
        <Text style={{ fontSize: '20px' }}>Commanders</Text>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
            {Object.keys(VelvetDawn.datapacks.entities)
                .filter(x => VelvetDawn.datapacks.entities[x].commander)
                .map(entity => {
                return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={entity}>
                    <Text style={{ paddingLeft: '12px' }}>{VelvetDawn.datapacks.entities[entity].name}</Text>
                    <div style={{display: 'flex', flexDirection: 'row'}}>
                        {!setup.commanders.includes(entity) && <Button style={{padding: ButtonPadding}} onClick={() => {
                            Api.setup.updateGameSetup(entity, 1).then(setSetup)
                        }}>Add</Button>}
                        {setup.commanders.includes(entity) && <Button style={{padding: ButtonPadding}} onClick={() => {
                            Api.setup.updateGameSetup(entity, 0).then(setSetup)
                        }}>Remove</Button>}
                    </div>
                </div>
            })}
        </div>

        <Text style={{ fontSize: '20px' }}>Units</Text>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
            {Object.keys(VelvetDawn.datapacks.entities)
                .filter(x => !VelvetDawn.datapacks.entities[x].commander)
                .map(entity => {
                return <div style={{
                    display: 'flex',
                    justifyContent: 'space-between'
                }} key={entity}>
                    <Text style={{ paddingLeft: '12px' }}>{VelvetDawn.datapacks.entities[entity].name}</Text>
                    <div style={{display: 'flex', flexDirection: 'row', gap: '8px', alignItems: 'center'}}>
                        <Button style={{padding: ButtonPadding}} onClick={() => {
                            Api.setup.updateGameSetup(entity, (setup.entities[entity] ?? 0) - 1).then(setSetup)
                        }}>-</Button>
                        <Text>{setup.entities[entity] ?? 0}</Text>
                        <Button style={{padding: ButtonPadding}} onClick={() => {
                            Api.setup.updateGameSetup(entity, (setup.entities[entity] ?? 0) + 1).then(setSetup)
                        }}>+</Button>
                    </div>
                </div>
            })}
        </div>
    </>
}


function NonAdminView({ setup }: { setup: GameSetup }) {
    return <>
        <Text style={{ fontSize: '20px' }}>Commanders</Text>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {setup.commanders.map((commander) => {
                return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={commander}>
                    <Text style={{ paddingLeft: '12px' }}>{VelvetDawn.datapacks.entities[commander].name}</Text>
                </div>
            })}
        </div>

        <Text style={{ fontSize: '20px' }}>Units</Text>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            {Object.keys(setup.entities).map((unit) => {
                return <div style={{ display: 'flex', justifyContent: 'space-between' }} key={unit}>
                    <Text style={{ paddingLeft: '12px' }}>{VelvetDawn.datapacks.entities[unit].name}</Text>
                    <Text>{setup.entities[unit]}</Text>
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
