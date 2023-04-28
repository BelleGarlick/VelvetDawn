package velvetdawn.mechanics.abilities;

import velvetdawn.VelvetDawn;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.anytype.AnyList;

import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class Abilities {

    public final HashMap<String, Ability> abilities = new HashMap<>();

    /** Get ability by its id */
    public Ability getById(String abilityId) {
        return abilities.get(abilityId);
    }

    public AnyList toJson() {
        return new AnyList(this.abilities.values().stream()
                .map(Ability::toJson)
                .collect(Collectors.toList()));
    }

    /** Parse the abilities list */
    public void load(VelvetDawn velvetDawn, String parentId, AnyList data) throws Exception {
        for (int i = 0; i < data.size(); i++) {
            var ability = Ability.fromJson(velvetDawn, parentId, i, data.get(i)
                    .validateInstanceIsJson(String.format("Error in %s. Abilities should be a list of json objects.", parentId)));
            this.abilities.put(ability.id, ability);
        }
    }
}
