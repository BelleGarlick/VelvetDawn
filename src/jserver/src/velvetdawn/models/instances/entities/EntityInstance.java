package velvetdawn.models.instances.entities;

import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.instances.Instance;
import velvetdawn.players.Player;

// Modified driving force - 25.7%
// Control 24.3%
// FBrake max 29.3%

public class EntityInstance extends Instance {

    public final Player player;

    public final Upgrades upgrades;
    public final Abilities abilities;
    public final Combat combat;

    public EntityInstance(VelvetDawn velvetDawn, Player player, String instanceId, String datapackId, Coordinate position) {
        super(datapackId, instanceId, position);

        this.player = player;

        this.upgrades = new Upgrades(velvetDawn, this);
        this.abilities = new Abilities(velvetDawn, this);
        this.combat = new Combat(velvetDawn, this);
    }
}
