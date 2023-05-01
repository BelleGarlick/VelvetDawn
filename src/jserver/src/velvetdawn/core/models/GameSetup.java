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

}
