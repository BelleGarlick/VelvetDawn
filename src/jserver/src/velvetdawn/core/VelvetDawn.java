package velvetdawn.core;

import velvetdawn.core.datapacks.DatapackManager;
import velvetdawn.core.entities.EntityManager;
import velvetdawn.core.game.Game;
import velvetdawn.core.map.MapManager;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.players.PlayerManager;
import velvetdawn.core.teams.TeamsManager;

public class VelvetDawn {

    public final DatapackManager datapacks = new DatapackManager();

    public final Game game;
    public final MapManager map;
    public final TeamsManager teams = new TeamsManager(this);
    public final PlayerManager players;
    public final EntityManager entities = new EntityManager(this);

    public VelvetDawn(Config config) throws Exception {
        this.game = new Game(this, config);
        this.map = new MapManager(this, config);
        this.players = new PlayerManager(this, config);

        this.datapacks.init(this, config);
    }

    public void save() {
        // todo propagate and implement
//        map.save();
//        teams.save();
//        players.save();
//        entities.save();
//        this.game.save();
    }
}
