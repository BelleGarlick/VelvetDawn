import {get, post} from "./utils";
import {AvailableUnitUpgradesAndAbilities, GameState, Position} from "models";


export function move(entityPk: string, path: Position[]): Promise<GameState> {
    return post("/units/move/", {
        "entity": entityPk,
        "path": JSON.stringify(path)
    })
}

export function getAvailableUpgradeAndAbilities(entityPk: string): Promise<AvailableUnitUpgradesAndAbilities> {
    return get(`/units/available-upgrades-and-abilities/?id=${entityPk}`)
}


export function performUpgrade(entityPk: string, upgradeId: string): Promise<AvailableUnitUpgradesAndAbilities> {
    return post("/units/upgrade/", {
        id: entityPk,
        upgrade: upgradeId
    })
}


export function performAbility(entityPk: string, abilityId: string): Promise<AvailableUnitUpgradesAndAbilities> {
    return post("/units/ability/", {
        id: entityPk,
        ability: abilityId
    })
}
