package velvetdawn.map.spawn;

import org.jetbrains.annotations.NotNull;
import velvetdawn.VelvetDawn;
import velvetdawn.models.Coordinate;
import velvetdawn.models.Team;
import velvetdawn.models.config.Config;
import velvetdawn.players.Player;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class BorderSpawnMode extends SpawnMode {

    Map<Player, Set<Coordinate>> allocation = new HashMap<>();

    /** Get the allocated spawn tiles for a given user */
    @Override
    public Set<Coordinate> getSpawnCoordinatesForPlayer(VelvetDawn velvetDawnCore, Config config, Player player) {
        return this.allocation.getOrDefault(player, Set.of());
    }

    @Override
    public void assignSpawnPoints(VelvetDawn velvetDawn, Config config) throws Exception {
        System.out.println("Allocating spawn area.");

        List<Team> teams = velvetDawn.teams.listWithoutSpectators();
        if (teams.isEmpty())
            throw new Exception("No teams to allocate spawn points for");

        // Count players per team to number of players per team
        var maxTeamSize = velvetDawn.teams.maxTeamSizeWithoutSpectators();

        // Calculate initial spawn points
        var spawns = getCentralSpawnOrdinates(
                config, teams.size(), maxTeamSize);

        var baseNeighbours = calculateSpawnBaseHalfWidth(config, maxTeamSize);
        for (int i = 0; i < spawns.size(); i++) {
            var spawnPoint = spawns.get(i);
            Set<Coordinate> spawnArea = new HashSet<>(Set.of(spawnPoint));

            for (int j = 0; j < calculateNeighbourDepth(config, maxTeamSize); j++) {
                for (Coordinate point: spawnArea)
                    spawnArea.addAll(velvetDawn.map.getNeighbours(point));
            }

            teams.get(i).listPlayersExcludeSpectators().forEach(player -> {
                this.allocation.put(player, spawnArea);
            });
        }
    }

    /** Calculate the number of initial sidewards neighbours before adding neighbour depth */
    private int calculateSpawnBaseHalfWidth(Config config, int maxTeamSize) {
        return config.spawn.spawnRadiusMultiplier * maxTeamSize + config.spawn.baseSpawnRadius + 1;
    }

    /** Calculate the number of neighbouring cell depth needed */
    private int calculateNeighbourDepth(Config config, int maxTeamSize) {
        return config.spawn.spawnRadiusMultiplier * maxTeamSize;
    }

    /** Calculate the half_width of the spawn areas defined by the config
     *
     * @param config Used to get spawning params
     * @param maxTeamSize Used to calculate the same spawn area size
     */
    private int calculateSpawnAreaHalfWidth(Config config, int maxTeamSize) {
        int width_either_side = calculateSpawnBaseHalfWidth(config, maxTeamSize);
        width_either_side += calculateNeighbourDepth(config, maxTeamSize);

        return width_either_side;
    }

    /** Calculate the central spawn ordinates of a spawn region for each team
     *
     * @param config The Game config
     * @param teamCount The number of teams in the game
     * @param maxTeamSize The max players in a team
     * @return List of co-ordinates that define the center of the spawn area
     */
    public List<Coordinate> getCentralSpawnOrdinates(Config config, int teamCount, int maxTeamSize) throws Exception {
        int mapSize = 1 + 2 * config.map.borderRadius;

        // Calculate non-spawnable width near the corners
        int insetPadding = calculateSpawnAreaHalfWidth(config, maxTeamSize);

        // Calc the number of perimeter cells that we cant to
        // distribute teams around
        int mapPerimeter = 4 * mapSize - 4;

        // Spacing between team cells
        int cornersRemoved = insetPadding > 0 ? 4 : 0;  // If 0 width then corner spawning is possible
        int spawnablePerimeterPositions = mapPerimeter
                - 4 * Math.min(mapSize, 2 * insetPadding)
                + cornersRemoved;
        if (spawnablePerimeterPositions <= 0)
            throw new Exception("Map too small for spawning constraints. Consider increasing the map size.");
        float gapBetweenTeams = spawnablePerimeterPositions / (float) teamCount;

        // The first teams spawn point and the current team
        // cell. Every time the current_team_point rounded up
        // equals the cell we're iteraing through, we mark this
        // cell as a spawn point and increase the new team mark
        var currentPoint = new Coordinate(0, -config.map.borderRadius);
        int currentTeamMark = 0;

        List<Coordinate> spawnPoints = new ArrayList<>();
        int perimeterCount = 0;

        int minMapOrd = -config.map.borderRadius + insetPadding;
        int maxMapOrd = config.map.borderRadius - insetPadding;

        for (int i = 0; i < mapPerimeter; i++) {
            Coordinate cell = getCellFromPerimeterIndex(config, i);
            if ((minMapOrd <= cell.x && cell.x <= maxMapOrd) || (minMapOrd <= cell.y && cell.y <= maxMapOrd)) {
                if (Math.floor(currentTeamMark) == perimeterCount) {
                    spawnPoints.add(currentPoint);
                    currentTeamMark += gapBetweenTeams;
                }
                perimeterCount += 1;
                currentPoint = getNextCoordinate(config, cell);
            }
        }

        return spawnPoints;
    }

    /** This function treats the perimeter as a band around the map
     * where each item is indexable starting in the top center at index 0
     *
     * @param config For getting the border and map size
     * @param perimeterIndex The index to get the coordinate for
     * @return The coordinate at that position
     */
    @NotNull
    public Coordinate getCellFromPerimeterIndex(@NotNull Config config, int perimeterIndex) {
        int mapRadius = config.map.borderRadius;

        if (perimeterIndex <= mapRadius)
            return new Coordinate(perimeterIndex, -config.map.borderRadius);
        else if (perimeterIndex <= 3 * mapRadius)
            return new Coordinate(config.map.borderRadius, perimeterIndex - 2 * config.map.borderRadius);
        else if (perimeterIndex <= 5 * mapRadius)
            return new Coordinate(-(perimeterIndex - 4 * config.map.borderRadius), config.map.borderRadius);
        else if (perimeterIndex <= 7 * mapRadius)
            return new Coordinate(-config.map.borderRadius, -(perimeterIndex - 6 * config.map.borderRadius));
        else
            return new Coordinate(perimeterIndex - 8 * config.map.borderRadius, -config.map.borderRadius);
    }

    /** This function will return the next point as we walk
     * around the perimeter of the map.
     *
     * This function works by treating the perimeter as a band
     * that the func walks along. So, first we convert the cell
     * to the perimeter, then move along the perimeter then
     * back to a cell.
     *
     * @param currentPoint The current point to get the next point for
     * @param config The velvet dawn config
     */
    public Coordinate getNextCoordinate(Config config, Coordinate currentPoint) {
        int mapSize = 1 + 2 * config.map.borderRadius;
        int totalPerimeterSize = 4 * mapSize - 4;

        // Convert cell to perimeter index
        int perimeterIndex = -1;
        if (currentPoint.tileY() == -config.map.borderRadius)
            perimeterIndex = (currentPoint.tileX() + totalPerimeterSize) % totalPerimeterSize;
        else if (currentPoint.tileX() == config.map.borderRadius)
            perimeterIndex = (currentPoint.tileY() + 2 * config.map.borderRadius);
        else if (currentPoint.tileY() == config.map.borderRadius)
            perimeterIndex = -(currentPoint.tileX() - (4 * config.map.borderRadius));
        else if (currentPoint.tileX() == -config.map.borderRadius)
            perimeterIndex = -(currentPoint.tileY() - (6 * config.map.borderRadius));

        // Shift perimeter index
        perimeterIndex += 1;
        perimeterIndex = (perimeterIndex + totalPerimeterSize) % totalPerimeterSize;

        // Convert perimeter index back to cell
        return getCellFromPerimeterIndex(config, perimeterIndex);
    }
}
