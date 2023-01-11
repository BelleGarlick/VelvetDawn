import {AvailableAbilities, UnitDefinition} from "models/entity";
import {ActionButton} from "./actionButton";
import * as Api from "api/index";
import {RenderingFacade} from "../../../facade";
import {PaginatedButtons} from "../../../entities/paginated-buttons";

export class UnitAbilities {

    private available: AvailableAbilities | undefined
    public unitAbilityButtons: { [abilityId: string]: ActionButton } = {}
    private paginatedButtons = new PaginatedButtons();

    setEntity(instanceId: number, uniDefinition: UnitDefinition) {
        this.paginatedButtons.resetTabPage()
        this.unitAbilityButtons = {};
        this.available = undefined

        uniDefinition.abilities.forEach(ability => {
            this.unitAbilityButtons[ability.id] = new ActionButton(ability.description)
                .text(ability.name)
                .icon(ability.icon)
                .onClick(() => {
                    Api.units.performAbility(instanceId, ability.id)
                })
        })
    }

    setAvailableAbilities(available: AvailableAbilities) {
        this.available = available;
    }

    render(facade: RenderingFacade, startY: number) {
        if (this.available) {
            const renderableButtons: ActionButton[] = []
            this.available.abilities.forEach((id) => {
                renderableButtons.push(this.unitAbilityButtons[id].enabled(true));
            })
            this.available.disabled.forEach((id) => {
                renderableButtons.push(this.unitAbilityButtons[id.abilityId].enabled(false).setReason(id.reason))
            })

            this.paginatedButtons.render(facade, renderableButtons, startY)
        }
    }
}
