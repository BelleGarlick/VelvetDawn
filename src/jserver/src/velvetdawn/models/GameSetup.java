package velvetdawn.models;

import lombok.Builder;
import lombok.Getter;

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
