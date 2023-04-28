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

    public BorderSpawnMode(VelvetDawn velvetDawn, Config config) {
        super(velvetDawn, config);
    }

    @Override
    public List<Coordinate> listAllSpawnPoints() {
        List<Coordinate> items = new ArrayList<>();
        this.allocation.values().forEach(items::addAll);
        return items;
    }

    /** Get the allocated spawn tiles for a given user */
    @Override
    public Set<Coordinate> getSpawnCoordinatesForPlayer(Player player) {
        return this.allocation.getOrDefault(player, Set.of());
    }

    @Override
    public void assignSpawnPoints() throws Exception {
        System.out.println("Allocating spawn area.");

        List<Team> teams = velvetDawn.teams.listWithoutSpectators();
        if (teams.isEmpty())
            throw new Exception("No teams to allocate spawn points for");

        // Count players per team to number of players per team
        var maxTeamSize = velvetDawn.teams.maxTeamSizeWithoutSpectators();

        // Calculate initial spawn points
        var spawns = getCentralSpawnOrdinates(teams.size(), maxTeamSize);

        for (int i = 0; i < spawns.size(); i++) {
            var spawnPoint = spawns.get(i);
            Set<Coordinate> spawnArea = new HashSet<>(Set.of(spawnPoint));

            for (int j = 0; j < calculateNeighbourDepth(maxTeamSize); j++) {
                for (Coordinate point: new HashSet<>(spawnArea))
                    spawnArea.addAll(velvetDawn.map.getNeighbours(point));
            }

            teams.get(i).listPlayersExcludeSpectators().forEach(player -> {
                this.allocation.put(player, spawnArea);
            });
        }
    }

    /** Calculate the number of initial sidewards neighbours before adding neighbour depth */
    public int calculateSpawnBaseHalfWidth(int maxTeamSize) {
        return config.spawn.spawnRadiusMultiplier * maxTeamSize + config.spawn.baseSpawnRadius + 1;
    }

    /** Calculate the number of neighbouring cell depth needed */
    private int calculateNeighbourDepth(int maxTeamSize) {
        return config.spawn.spawnRadiusMultiplier * maxTeamSize;
    }

    /** Calculate the central spawn ordinates of a spawn region for each team
     *
     * @param teamCount The number of teams in the game
     * @param maxTeamSize The max players in a team
     * @return List of co-ordinates that define the center of the spawn area
     */
    public List<Coordinate> getCentralSpawnOrdinates(int teamCount, int maxTeamSize) throws Exception {
        // Calculate non-spawnable width near the corners
        int insetPadding = calculateSpawnBaseHalfWidth(maxTeamSize);

        // Calc the number of perimeter cells that we cant to
        // distribute teams around
        int mapPerimeter = this.getTotalPerimeterSize();

        // Spacing between team cells
        int cornersRemoved = insetPadding > 0 ? 4 : 0;  // If 0 width then corner spawning is possible
        int spawnablePerimeterPositions = mapPerimeter
                - 2 * Math.min(config.map.width, 2 * insetPadding)
                - 2 * Math.min(config.map.height, 2 * insetPadding)
                + cornersRemoved;
        if (spawnablePerimeterPositions <= 0)
            throw new Exception("Map too small for spawning constraints. Consider increasing the map size.");
        float gapBetweenTeams = spawnablePerimeterPositions / (float) teamCount;

        // The first teams spawn point and the current team
        // cell. Every time the current_team_point rounded up
        // equals the cell we're iteraing through, we mark this
        // cell as a spawn point and increase the new team mark
        var currentPoint = new Coordinate((float) (config.map.width / 2), 0);
        float currentTeamMark = 0;

        List<Coordinate> spawnPoints = new ArrayList<>();
        int perimeterCount = 0;

        for (int i = config.map.width / 2; i < mapPerimeter + config.map.width / 2; i++) {
            var cell = getCellFromPerimeterIndex(i % mapPerimeter);
            if (
                    (insetPadding <= cell.x && cell.x < config.map.width - insetPadding)
                || (insetPadding <= cell.y && cell.y < config.map.height - insetPadding)
            ) {
                if (Math.floor(currentTeamMark) == perimeterCount) {
                    spawnPoints.add(currentPoint);
                    currentTeamMark += gapBetweenTeams;
                }
                perimeterCount += 1;

                currentPoint = getNextCoordinate(cell);
            }
        }

        return spawnPoints;
    }

    /** This function treats the perimeter as a band around the map
     * where each item is indexable starting in the top center at index 0
     *
     * @param perimeterIndex The index to get the coordinate for
     * @return The coordinate at that position
     */
    @NotNull
    public Coordinate getCellFromPerimeterIndex(int perimeterIndex) {
        int width = config.map.width;
        int height = config.map.height;

        if (perimeterIndex < width)
            return new Coordinate(perimeterIndex, 0);
        else if (perimeterIndex < width + height - 1)
            return new Coordinate(width - 1, perimeterIndex - (width - 1));
        else if (perimeterIndex < width + height + width - 2)
            return new Coordinate(width - 1 - (perimeterIndex - (height + width - 2)), height - 1);
        else
            return new Coordinate(0, height - 1 - (perimeterIndex - (height + width + width - 3)));
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
     */
    public Coordinate getNextCoordinate(Coordinate currentPoint) {
        int width = config.map.width;
        int height = config.map.height;

        int perimeterIndex = 0;

        // Convert cell to perimeter index
        if (currentPoint.y == 0)
            perimeterIndex = (int) currentPoint.x;
        else if (currentPoint.x == width - 1)
            perimeterIndex = (int) (currentPoint.y + width - 1);
        else if (currentPoint.y == height - 1)
            perimeterIndex = (int) ((width + height - 2) + (width - currentPoint.x - 1));
        else if (currentPoint.x == 0)
            perimeterIndex = (int) ((width + height + width - 3) + (height - currentPoint.y - 1));

        // Shift perimeter index
        perimeterIndex += 1;
        perimeterIndex = (perimeterIndex + this.getTotalPerimeterSize()) % this.getTotalPerimeterSize();

        // Convert perimeter index back to cell
        return getCellFromPerimeterIndex(perimeterIndex);
    }

    private int getTotalPerimeterSize() {
        return 2 * config.map.height + 2 * config.map.width - 4;
    }
}
