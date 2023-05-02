import {get, post} from "./utils";
import {AvailableUnitUpgradesAndAbilities, GameState, Position} from "models";


export function move(entityPk: string, path: Position[]): Promise<GameState> {
    return post("/entities/move/", {
        "instanceId": entityPk,
        "path": JSON.stringify({path: path})
    })
}

export function getAvailableUpgradeAndAbilities(entityPk: string): Promise<AvailableUnitUpgradesAndAbilities> {
    return get(`/entities/available-upgrades-and-abilities/?instanceId=${entityPk}`)
}


export function performUpgrade(entityPk: string, upgradeId: string): Promise<AvailableUnitUpgradesAndAbilities> {
    return post("/entities/upgrade/", {
        instanceId: entityPk,
        upgradeId: upgradeId
    })
}


export function performAbility(entityPk: string, abilityId: string): Promise<AvailableUnitUpgradesAndAbilities> {
    return post("/entities/ability/", {
        instanceId: entityPk,
        abilityId: abilityId
    })
}
