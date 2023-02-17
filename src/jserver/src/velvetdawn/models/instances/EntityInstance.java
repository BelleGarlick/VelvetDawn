package velvetdawn.models.instances;

import velvetdawn.models.Coordinate;
import velvetdawn.players.Player;

// Modified driving force - 25.7%
// Control 24.3%
// FBrake max 29.3%

public class EntityInstance extends Instance {

    public final Player player;

    public EntityInstance(Player player, String instanceId, String datapackId, Coordinate position) {
        super(datapackId, instanceId, position);

        this.player = player;
    }
}
