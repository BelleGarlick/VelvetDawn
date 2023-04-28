package velvetdawn;

import velvetdawn.datapacks.DatapackManager;
import velvetdawn.entities.EntityManager;
import velvetdawn.game.Game;
import velvetdawn.map.MapManager;
import velvetdawn.models.config.Config;
import velvetdawn.players.PlayerManager;
import velvetdawn.teams.TeamsManager;

public class VelvetDawn {

    private final Config config;

    public final DatapackManager datapacks = new DatapackManager();

    public final Game game;
    public final MapManager map;
    public final TeamsManager teams = new TeamsManager(this);
    public final PlayerManager players;
    public final EntityManager entities = new EntityManager(this);

    public VelvetDawn(Config config) throws Exception {
        this.config = config;

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
