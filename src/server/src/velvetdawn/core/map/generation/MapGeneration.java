package velvetdawn.core.map.generation;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.config.Config;
import velvetdawn.core.models.instances.TileInstance;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.stream.Collectors;

public class MapGeneration {

    private final VelvetDawn velvetDawn;
    private final Config config;

    public MapGeneration(VelvetDawn velvetDawn, Config config) {
        this.velvetDawn = velvetDawn;
        this.config = config;
    }

    public ArrayList<ArrayList<TileInstance>> generate() throws Exception {
        Random random = new Random();
        System.out.printf("Creating map with seed: %s.%n", config.map.seed);
        random.setSeed(config.map.seed);

        var map = new CollapsingMap(velvetDawn, config);

        List<Coordinate> uncheckedCells = new ArrayList<>();
        for (int x = 0; x < config.map.width; x++) {
            for (int y = 0; y < config.map.height; y++)
                uncheckedCells.add(new Coordinate(x, y));
        }

        Coordinate nextCell = getNextTile(random, uncheckedCells);
        int i = 0;
        while (nextCell != null) {
            if (i % 250 == 0)
                System.out.printf("\r%s/%s\n", i, config.map.width * config.map.height);
            i += 1;
            collapseCell(random, map, nextCell);
            nextCell = getNextTile(random, uncheckedCells);
        }
        System.out.println("Completed.");

        return map.toTiles();
    }

    private void printMap(CollapsingMap map) {
        for (int i = 0; i < map.map.size(); i++) {
            var row = map.map.get(i);
            for (int j = 0; j < row.size(); j++) {
                int count = row.get(j).size();
                System.out.print(count + (count >= 10 ? " " : "  "));
            }
            System.out.println();
        }
        System.out.println();
    }

    private Coordinate getNextTile(Random random, List<Coordinate> uncheckedCells) {
        if (uncheckedCells.isEmpty())
            return null;

        int i = random.nextInt(uncheckedCells.size());
        Coordinate cell = uncheckedCells.get(i);
        uncheckedCells.remove(i);
        return cell;
    }

    private Set<String> getPossibleNeighbours(Set<String> cellOptions) {
        Set<String> possibleTiles = new HashSet<>();
        cellOptions.forEach(option -> {
            possibleTiles.addAll(velvetDawn.datapacks.tiles.get(option).neighbours.keys());
        });

        return possibleTiles;
    }

    public void collapseCell(Random random, CollapsingMap map, Coordinate cell) throws Exception {
        // TODO Only get probabilities from fully collapsed cells
        List<String> collapsedCellProbs = new ArrayList<>();
        var cellProbabilites = getNeighbouringCellProbabilities(velvetDawn, map, cell);
        cellProbabilites.forEach((key, count) -> {
            for (int i = 0; i < count; i++)
                collapsedCellProbs.add(key);
        });

        var randomIndex = random.nextInt(collapsedCellProbs.size());
        var cellChoise = collapsedCellProbs.get(randomIndex);

        map.set(cell, new HashSet<>(Set.of(cellChoise)));
        var possibleNeighbours = getPossibleNeighbours(map.get(cell));

        ArrayList<NeighbourInformation> neighbourUpdates = new ArrayList<>(List.of(
                new NeighbourInformation(
                        possibleNeighbours,
                        velvetDawn.map.getNeighbours(cell)
                )
        ));

        while (!neighbourUpdates.isEmpty()) {
            NeighbourInformation neighbours = neighbourUpdates.get(0);
            neighbourUpdates.remove(0);

            for (Coordinate neighbour: neighbours.cells) {
                if (map.get(neighbour) == null)
                    continue;

                int currentPossibilities = map.get(neighbour).size();
                map.get(neighbour).retainAll(neighbours.possibleNeighbours);
                if (map.get(neighbour).isEmpty())
                    throw new Exception("Error on map generation");

                if (map.get(neighbour).size() < currentPossibilities) {
                    // TODO Only add neighbours if in range
                    neighbourUpdates.add(new NeighbourInformation(
                            getPossibleNeighbours(map.get(neighbour)),
                            velvetDawn.map.getNeighbours(neighbour)
                    ));
                }
            }
        }

        // print()
        // for r in range(len(map[0])):
        //     for c in range(len(map)):
        //         print(str(len(map[c][r])) + " ", end="")
        //     print()
        //
        // breakpoint()
    }

    public Map<String, Integer> getNeighbouringCellProbabilities(VelvetDawn velvetDawn, CollapsingMap map, Coordinate cell) throws Exception {
        Map<String, Integer> probabilityMap = map.get(cell).stream().collect(Collectors.toMap(key -> key, key -> 0));
        List<Coordinate> neighbouringCellCoords = velvetDawn.map.getNeighbours(cell);

        for (Coordinate coord: neighbouringCellCoords) {
            var possibleTiles = map.get(coord);
            if (possibleTiles == null)
                continue;

            if (possibleTiles.size() > 1)
                continue;

            Map<String, Integer> weightedPossibleNeighbours = new HashMap<>();
            for (String tile: possibleTiles) {
                var tileDef = velvetDawn.datapacks.tiles.get(tile);
                for (String tileKey: tileDef.neighbours.keys()) {
                    weightedPossibleNeighbours.put(
                            tileKey,
                            (int) (weightedPossibleNeighbours.getOrDefault(tileKey, 0)
                                                        + velvetDawn.datapacks.tiles.get(tile).neighbours.get(tileKey).toNumber())
                    );
                }
            }

            new ArrayList<>(probabilityMap.keySet()).forEach(key -> {
                if (!weightedPossibleNeighbours.containsKey(key))
                    probabilityMap.remove(key);
                else {
                    probabilityMap.put(
                            key,
                            probabilityMap.getOrDefault(key, 0)
                                    + weightedPossibleNeighbours.getOrDefault(key, 0)
                    );
                }
            });
        }

        // Check the sum of values is greater than 0, if not set probability of all to 1.
        int probabilitySum = 0;
        for (int value: probabilityMap.values())
            probabilitySum += value;
        if (probabilitySum == 0) {
            probabilityMap.replaceAll((k, v) -> 1);
        }

        return probabilityMap;
    }

    private static class NeighbourInformation {
        Set<String> possibleNeighbours;
        List<Coordinate> cells;

        public NeighbourInformation(Set<String> possibleNeighbours, List<Coordinate> cells) {
            this.possibleNeighbours = possibleNeighbours;
            this.cells = cells;
        }
    }
}
