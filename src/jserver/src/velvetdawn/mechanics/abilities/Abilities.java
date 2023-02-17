package velvetdawn.mechanics.abilities;

import velvetdawn.VelvetDawn;
import velvetdawn.utils.Json;

import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class Abilities {

    private final HashMap<String, Ability> abilities = new HashMap<>();

    /** Get ability by its id */
    public Ability getById(String abilityId) {
        return abilities.get(abilityId);
    }

    public List<Json> toJson() {
        return this.abilities.values().stream()
                .map(Ability::toJson)
                .collect(Collectors.toList());
    }

    /** Parse the abilities list */
    public void load(VelvetDawn velvetDawn, String parentId, List<Json> data) throws Exception {
        for (int i = 0; i < data.size(); i++) {
            var ability = Ability.fromJson(velvetDawn, parentId, i, data.get(i));
            this.abilities.put(ability.id, ability);
        }
    }
}
