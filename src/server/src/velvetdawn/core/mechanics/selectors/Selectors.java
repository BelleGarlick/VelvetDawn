package velvetdawn.core.mechanics.selectors;

import velvetdawn.core.VelvetDawn;
import velvetdawn.core.mechanics.selectors.tiles.SelectorTile;
import velvetdawn.core.mechanics.selectors.tiles.SelectorTiles;

import java.util.List;

public class Selectors {

    /* Selectors module

    This is the entry point to load a selectors module based on the
    selector string ('local[range=10].health.max'). The get_selector
    function will load the suitable select for which the function
    is called for.
    */

    // todo more documentation and testing

    /** Parse a selector string.
     * This works by separating out the chains, setting the
     * tags and setting the attributes
     *
     * @param parentId Shown to the user if an error is raised
     * @param selector String to parse
     */
    public static Selector get(VelvetDawn velvetDawn, String parentId, String selector) throws Exception {
        String selectorString = selector.replace(" ", "");
        Selector head = null;
        Selector last = null;

        for (String chain: selectorString.split(">")) {
            String selectorName;
            List<String> filters = List.of();
            String attribute = null;

            // Parse the selectors
            if (chain.contains("[")) {
                String[] tokens = chain.split("\\[");
                List<String> filtersAndAttributes = List.of(tokens[1].split("]"));
                selectorName = tokens[0];
                filters = filtersAndAttributes.size() > 0
                    ? List.of(filtersAndAttributes.get(0).replace(" ", "").split(","))
                    : null;

                if (filtersAndAttributes.size() > 1)
                    attribute = filtersAndAttributes.get(1).substring(1);

            } else {
                List<String> tokens = List.of(chain.split("\\."));
                selectorName = tokens.get(0);
                if (tokens.size() > 1)
                    attribute = String.join(".", tokens.subList(1, tokens.size()));
            }

            // Load selector for the given type
            Selector selectorObj = assignFilters(
                    Selectors.getSelectorByKey(velvetDawn, selectorName),
                    filters
            );

            if (head == null) head = selectorObj;
            if (last != null) last.chainedSelector = selectorObj;
            last = selectorObj;

            head.attribute = attribute;
        }

        if (head == null)
            throw new Exception(String.format("Problem with selector '%s' detected.", selectorString));

        return head;
    }

    private static Selector getSelectorByKey(VelvetDawn velvetDawn, String key) throws Exception {
        switch (key) {
            case "self":
                return new SelectorSelf(velvetDawn);
            case "world":
                return new WorldSelector(velvetDawn);
            case "tile":
                return new SelectorTile(velvetDawn);
            case "tiles":
                return new SelectorTiles(velvetDawn);
            case "entity":
                return new SelectorUnit(velvetDawn);
            case "entities":
                return new SelectorEntities(velvetDawn);
            case "friendlies":
                return new SelectorFriendlies(velvetDawn);
            case "enemies":
                return new SelectorEnemies(velvetDawn);
        }

        throw new Exception(String.format("Invalid selector: '%s'", key));
    }

    /** Instantiate a selector with the filters and attribute
     *
     * @param filters The full filters being parsed
     * @return The new selector
     */
    private static Selector assignFilters(Selector selector, List<String> filters) throws Exception {
        if (!filters.isEmpty()) {
            for (String filter: filters) {
                if (filter.contains("=")) {
                    String[] filterTokens = filter.split("=");
                    if (filterTokens.length == 2)
                        selector.filters.addFilter(filterTokens[0], filterTokens[1]);
                    else
                        throw new Exception(String.format("Invalid filter: %s", filter));
                } else
                    selector.filters.addFilter(filter);
            }
        }

        return selector;
    }
}
