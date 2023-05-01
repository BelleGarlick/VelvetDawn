package velvetdawn.core.models;

import lombok.Builder;
import lombok.Getter;

@Builder
@Getter
public class TurnData {
    private Team activeTurn;
    private Long currentTurnTime;
    private Long turnStart;
}
