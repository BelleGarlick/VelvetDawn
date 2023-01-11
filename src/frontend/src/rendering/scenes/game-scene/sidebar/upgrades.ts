import {AvailableUpgrades, UnitDefinition} from "models/entity";
import {ActionButton} from "./actionButton";
import * as Api from "api/index";
import {RenderingFacade} from "../../../facade";
import {PaginatedButtons} from "../../../entities/paginated-buttons";

export class UnitUpgrades {

    private available: AvailableUpgrades | undefined
    public unitUpgradeButtons: { [upgradeId: string]: ActionButton } = {}
    private paginatedButtons = new PaginatedButtons();

    setEntity(instanceId: number, uniDefinition: UnitDefinition) {
        this.paginatedButtons.resetTabPage()
        this.unitUpgradeButtons = {};
        this.available = undefined

        uniDefinition.upgrades.forEach(upgrade => {
            this.unitUpgradeButtons[upgrade.id] = new ActionButton(upgrade.description)
                .text(upgrade.name)
                .icon(upgrade.icon)
                .onClick(() => {
                    Api.units.performUpgrade(instanceId, upgrade.id)
                })
        })
    }

    setAvailableUpgrades(available: AvailableUpgrades) {
        this.available = available;
    }

    render(facade: RenderingFacade, startY: number) {
        if (this.available) {
            const renderableButtons: ActionButton[] = []
            this.available.upgrades.forEach((id) => {
                renderableButtons.push(this.unitUpgradeButtons[id].enabled(true));
            })
            this.available.disabled.forEach((id) => {
                renderableButtons.push(this.unitUpgradeButtons[id.upgradeId].enabled(false).setReason(id.reason))
            })
            this.available.missingRequirements.forEach((id) => {
                renderableButtons.push(this.unitUpgradeButtons[id.upgradeId].enabled(false).setReason(id.reason))
            })
            this.available.upgraded.forEach((id) => {
                renderableButtons.push(this.unitUpgradeButtons[id].used())
            })

            this.paginatedButtons.render(facade, renderableButtons, startY)
        }
    }
}
