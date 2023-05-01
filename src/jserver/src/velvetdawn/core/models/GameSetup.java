package velvetdawn.core.models;

import lombok.Builder;
import lombok.Getter;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.models.anytype.AnyList;
import velvetdawn.core.models.anytype.AnyString;

import java.util.Map;
import java.util.Set;

@Builder
@Getter
public class GameSetup {

    private Set<String> commanders;
    private Map<String, Integer> entities;
    private boolean commanderPlaced;
    private Map<String, Integer> remainingEntities;

    public AnyJson json() {
        var commanders = new AnyList();
        var entities = new AnyJson();
        var remainingEntities = new AnyJson();

        this.commanders.forEach(id -> commanders.add(new AnyString(id)));
        this.entities.forEach(entities::set);
        this.entities.forEach(entities::set);

        return new AnyJson()
                .set("commanders", commanders)
                .set("entities", entities)
                .set("commanderPlaced", this.commanderPlaced)
                .set("remainingEntities", remainingEntities);
    }
}
