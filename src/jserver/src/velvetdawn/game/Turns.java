package velvetdawn.game;

import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;
import velvetdawn.models.Phase;
import velvetdawn.models.Team;
import velvetdawn.models.TurnData;
import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.models.instances.entities.EntityInstance;
import velvetdawn.models.instances.TileInstance;
import velvetdawn.models.instances.WorldInstance;
import velvetdawn.players.Player;

import java.util.Collection;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;

public class Turns {

    private final VelvetDawn velvetDawn;
    private final Config config;

    private Team activeTurn;
    private Long turnStartTime;

    public Turns(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;
    }

    /** Get the current turn.
     *
     * If not in the game phase then no-one has the turn
     * otherwise, try to load from the key or set to
     * the first team.
     *
     * @return Current turn.
     */
    public Team getActiveTurn() {
        if (velvetDawn.game.phase != Phase.Game)
            return null;

        return this.activeTurn;
    }

    /** Get the current turn data returned to the user
     *
     * Args:
     *     config: To get the current turn time
     *     current_phase: The current phase of the game
     *
     * Returns:
     *     TurnData to include the current turn number, player's turn
     *     when the turn started and how long the turn is
     */
    public TurnData currentTurnData() {
        if (this.turnStartTime == null)
            this.updateTurnStartTime();

        return TurnData
                .builder()
                .activeTurn(this.getActiveTurn())
                .currentTurnTime(this.currentTurnTime())
                .turnStart(this.turnStartTime)
                .build();
    }

    /** Ready a player but if the phase is setup then check they've placed a commander */
    public void ready(Player player) throws Exception {
        if (velvetDawn.game.phase == Phase.Setup) {
            var setup = velvetDawn.game.setup.getSetup(player);
            if (!setup.isCommanderPlaced())
                throw new Exception("You must place your commander.");
        }

        System.out.printf("Player '%s' ready.%n", player.name);
        player.ready = true;
    }

    /** Mark a player as not ready */
    public void unready(Player player) {
        System.out.printf("Player '%s' unready.%n", player.name);
        player.ready = false;
    }

    /** Check if the end-turn case has occured either by the turn
     * running of player's reading-up.
     *
     * The function should only be called when the host get the
     * game state.
     *
     * This will trigger the next turn to occur if true or the
     * game to begin.
     */
    public void checkEndTurnCase() throws Exception {
        if (velvetDawn.game.phase == Phase.Lobby || velvetDawn.game.phase == Phase.GameOver)
            return;

        if (this.checkAllPlayersReady()) {
            System.out.println("All players ready.");
            if (velvetDawn.game.phase == Phase.Setup)
                velvetDawn.game.startGamePhase();
            else if (velvetDawn.game.phase == Phase.Game)
                this.beginNextTurn();
        }

        var currentTime = System.currentTimeMillis();
        var startTime = this.turnStartTime != null ? this.turnStartTime : this.updateTurnStartTime();
        var allowedTurnTime = this.currentTurnTime();

        if (currentTime > startTime + allowedTurnTime) {
            System.out.printf("%s has elapsed in setup, moving to next turn%n", allowedTurnTime);
            if (velvetDawn.game.phase == Phase.Setup)
                velvetDawn.game.startGamePhase();
            else if (velvetDawn.game.phase == Phase.Game)
                this.beginNextTurn();
        }
    }

    /** Start the next turn by:
     *   - Marking all players as not ready
     *   - set the next teams turn
     *   - save the whole game
     *   - update the turn timer
     *   - update the remaining movement of all entities to their range
     */
    public void beginNextTurn() throws Exception {
        List<Team> teams = velvetDawn.teams.listWithoutSpectators();
        velvetDawn.players.list().forEach(player -> player.ready = false);

        // Find the next team's turn
        // If current none, default to the last team for when looped through, else loop through and find the next iteration
        var currentTurn = this.getActiveTurn();

        // If there is a turn, then trigger the end turn actions, otherwise it means there
        // is no turn as the game has only just begin
        if (currentTurn != null)
            this.triggerOnTurnEndActions(currentTurn);
        else
            currentTurn = teams.get(teams.size() - 1);

        velvetDawn.save();

        Team newTeamTurn = null;
        for (int i = 0; i < teams.size(); i++) {
            var team = teams.get(i);
            if (team == currentTurn)
                newTeamTurn = teams.get((i + 1) % teams.size());
        }

        this.activeTurn = newTeamTurn;

        // Update turn's player's entities to reset there remaining moves
        assert newTeamTurn != null;
        velvetDawn.entities.all().forEach(entity ->
            entity.attributes.set(
                    "movement.remaining",
                    entity.attributes.get("movement.range", new AnyFloat(1))
            ));

        // Fire triggers on turn begins
        if (newTeamTurn == teams.get(0))
            this.triggerOnRoundBeginActions();
        triggerOnTurnBeginActions(newTeamTurn);

        this.updateTurnStartTime();
    }

    /** Trigger all entity/tile round being actions */
    public void triggerOnRoundBeginActions() throws Exception {
        for (EntityInstance entity: velvetDawn.entities.list())
            velvetDawn.datapacks.entities.get(entity.datapackId).triggers.onRound(entity);

        for (TileInstance tile: velvetDawn.map.listTiles())
            velvetDawn.datapacks.tiles.get(tile.datapackId).triggers.onRound(tile);

        velvetDawn.datapacks.world.triggers.onRound(WorldInstance.getInstance());
    }

    /** Trigger all entity/tile turn begin actions
     *
     * Testing for this exists in the triggers test suite
     *
     * @param newTeamTurn The team whos turn is starting
     */
    public void triggerOnTurnBeginActions(Team newTeamTurn) throws Exception {
        var playerBreakdown = velvetDawn.players.getFriendlyEnemyPlayersBreakdown(newTeamTurn);

        for (EntityInstance entity: velvetDawn.entities.list()) {
            var entityDef = velvetDawn.datapacks.entities.get(entity.datapackId);
            entityDef.triggers.onTurn(entity);

            if (playerBreakdown.friendlyPlayers.contains(entity.player))
                entityDef.triggers.onFriendlyTurn(entity);

            if (playerBreakdown.enemyPlayers.contains(entity.player))
                entityDef.triggers.onEnemyTurn(entity);
        }

        for (TileInstance tile: velvetDawn.map.listTiles())
            velvetDawn.datapacks.tiles.get(tile.datapackId).triggers.onTurn(tile);

        velvetDawn.datapacks.world.triggers.onTurn(WorldInstance.getInstance());
    }

    /** Trigger all entity/tile turn end actions
     *
     * Testing for this exists in the triggers test suite
     *
     * @param lastTurnsTeam The team who's turn is ending
     */
    private void triggerOnTurnEndActions(Team lastTurnsTeam) throws Exception {
        var playerBreakdown = velvetDawn.players.getFriendlyEnemyPlayersBreakdown(lastTurnsTeam);

        for (EntityInstance entity: velvetDawn.entities.list()) {
            var entityDef = velvetDawn.datapacks.entities.get(entity.datapackId);
            entityDef.triggers.onTurnEnd(entity);

            if (playerBreakdown.friendlyPlayers.contains(entity.player))
                entityDef.triggers.onFriendlyTurnEnd(entity);

            if (playerBreakdown.enemyPlayers.contains(entity.player))
                entityDef.triggers.onEnemyTurnEnd(entity);
        }

        for (TileInstance tile: velvetDawn.map.listTiles())
            velvetDawn.datapacks.tiles.get(tile.datapackId).triggers.onTurnEnd(tile);

        velvetDawn.datapacks.world.triggers.onTurnEnd(WorldInstance.getInstance());
    }

    /** Check all players are ready for the current team/turn.
     *
     * @return True if all players are ready.
     */
    public boolean checkAllPlayersReady() {
        AtomicBoolean allReady = new AtomicBoolean(true);

        Collection<Player> players = List.of();
        if (velvetDawn.game.phase == Phase.Setup)
            players = velvetDawn.players.listWithoutSpectators();

        else if (velvetDawn.game.phase == Phase.Game)
            players = this.getActiveTurn().listPlayersExcludeSpectators();

        players.forEach(player -> allReady.set(allReady.get() && player.ready));

        return allReady.get();
    }

    /** Update the time the current turn started to the current time */
    public long updateTurnStartTime() {
        return this.turnStartTime = System.currentTimeMillis();
    }

    /** Return config turn time unless in setup phase */
    public long currentTurnTime() {
        return velvetDawn.game.phase == Phase.Setup
                ? config.setupTime
                : config.turnTime;
    }
}
