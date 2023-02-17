package velvetdawn.players;

import org.jetbrains.annotations.NotNull;
import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;
import velvetdawn.models.Team;
import velvetdawn.models.instances.EntityInstance;
import velvetdawn.models.instances.Instance;
import velvetdawn.utils.Json;

import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class PlayerManager {

    private final VelvetDawn velvetDawn;
    private final Config config;

    private final Map<String, Player> players = new HashMap<>();

    public PlayerManager(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;
    }

    public Collection<Player> list() {
        return this.players.values();
    }

    public Collection<Player> listWithoutSpectators() {
        return this.players
                .values()
                .stream()
                .filter(player -> !player.spectating)
                .collect(Collectors.toList());
    }

    public Player getPlayer(String playerName) {
        return this.players.get(playerName);
    }

    /** Join the server.
     *
     * First check the name is not matches regex, then load the player
     * if the player doesn't exist then create the player and balance
     * the teams.
     *
     * If the player does exist then check the password matches
     *
     * @param playerName The username of the user joining the server
     * @param password The user's password
     */
    public Player join(String playerName, @NotNull String password) throws Exception {
        Pattern pattern = Pattern.compile("^[a-zA-Z0-9]{3,8}$");
        Matcher matcher = pattern.matcher(playerName);
        if (!matcher.find()) {
            throw new Exception("Names must be 3-8 characters long and letters & numbers only");
        }

        var player = this.getPlayer(playerName);
        if (player == null)
            player = new Player(playerName, password, this.players.size() == 0);
        else if (!player.password.equals(password))
            throw new Exception("Incorrect password");

        this.players.put(playerName, player);

        // Update teams to balance players
        velvetDawn.teams.autoUpdate();

        return player;
    }

    public void disconnect(VelvetDawn velvetDawn, Config config, Player player) {
        this.save(config, player);
        this.players.remove(player.name);
        velvetDawn.entities.removeForPlayer(player);
        // todo if a player hasn't pinged in 30s then this should be called
    }

    /** Get the sets of friendly and enemy players from
     * the perspective of the given team. Spectators are
     * not included
     *
     * @param team The team object
     */
    public FriendlyEnemyPlayersBreakDown getFriendlyEnemyPlayersBreakdown(Team team) {
        var breakdown = new FriendlyEnemyPlayersBreakDown();

        this.listWithoutSpectators().forEach(player -> {
            if (player.team == team)
                breakdown.friendlyPlayers.add(player);
            else
                breakdown.enemyPlayers.add(player);
        });

        return breakdown;
    }

    public FriendlyEnemyPlayersBreakDown getFriendlyEnemyPlayersBreakdownForInstance(Instance instance) {
        if (instance instanceof EntityInstance)
            return this.getFriendlyEnemyPlayersBreakdown(((EntityInstance) instance).player.team);

        return getFriendlyEnemyPlayersBreakdown(velvetDawn.game.turns.getActiveTurn());
    }

    public void saveAll(Config config) {
        for (Player player: this.players.values()) {
            this.save(config, player);
        }
    }

    public void save(Config config, Player player) {
        var json = player.toJson();
        config.getWorldSavePath().getChild("players").getChild(player.name + ".json").saveJson(json);
    }

    public void load(Config config, String playerName) throws Exception {
        Json playerJson = config.getWorldSavePath().getChild("players").getChild(playerName + ".json").loadAsJson();
        var player = Player.fromJson(playerJson);
        this.players.put(player.name, player);
    }

    public static class FriendlyEnemyPlayersBreakDown {
        public Set<Player> friendlyPlayers = new HashSet<>();
        public Set<Player> enemyPlayers = new HashSet<>();
    }
}
