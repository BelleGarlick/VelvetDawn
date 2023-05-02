

export interface EntityDefinition {
    datapackId: string
    name: string
    description: string
    commander: boolean,
    textures: {
        background: string
    },
    attributes: {
        icon: string | undefined
        name: string | undefined
        id: string
    }[],
    abilities: { id: string, icon: string, name: string, description: string }[],
    upgrades: { id: string, icon: string, name: string, description: string }[]
}
export type UnitDefinition = EntityDefinition;


export interface AvailableUpgrades {
    instance: number,
    hidden: {upgradeId: string, reason: string}[],
    disabled: {upgradeId: string, reason: string}[],
    missingRequirements: {upgradeId: string, reason: string}[],
    upgrades: string[],
    upgraded: string[]
}
export interface AvailableAbilities {
        instance: number,
        hidden: {abilityId: string, reason: string}[],
        disabled: {abilityId: string, reason: string}[],
        abilities: string[]
}

export interface AvailableUnitUpgradesAndAbilities {
    upgrades: AvailableUpgrades;
    abilities: AvailableAbilities;
}
