package velvetdawn.datapacks;

import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyBool;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.anytype.AnyList;
import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;
import velvetdawn.models.datapacks.entities.EntityDefinition;
import velvetdawn.models.datapacks.ResourceDefinition;
import velvetdawn.models.datapacks.tiles.TileDefinition;
import velvetdawn.models.datapacks.WorldDefinition;
import velvetdawn.utils.Path;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;


public class DatapackManager {

    public final Map<String, AnyJson> abstractDefinitions = new HashMap<>();
    public final Map<String, EntityDefinition> entities = new HashMap<>();
    public final Map<String, TileDefinition> tiles = new HashMap<>();
    public final Map<String, ResourceDefinition> resources = new HashMap<>();
    public final WorldDefinition world = new WorldDefinition();

    private final static Set<String> BUILT_IN = Set.of("__testing__", "base");

    public void init(VelvetDawn velvetDawn, Config config) throws Exception {
        for (String datapack: config.datapacks) {
            loadDatapack(
                    velvetDawn,
                    config.getDatapackPath().getChild(datapack),
                    datapack
            );
        }
    }

    private void loadDatapack(VelvetDawn velvetDawn, Path datapackPath, String datapackId) throws Exception {
        System.out.println("Loading datapack " + datapackId);

        var path = datapackPath;
        var packId = datapackId;

        if (datapackId.equals("__testing__")) {
            packId = "testing";
            path = new Path("./src/velvetdawn/datapacks/built-in/__testing__");
        }
        if (datapackId.equals("base"))
            path = new Path("./src/velvetdawn/datapacks/built-in/base");

        // TODO
//        if (!datapackPath.exists())
//            throw ValidationError("Datapack '{datapack}' not found.");


        loadDatapackMetadata(velvetDawn, path, packId);

        loadResources(path.getChild("resources"), packId);
        loadTiles(velvetDawn, path.getChild("tiles"), packId);
        loadEntities(velvetDawn, path.getChild("entities"), packId);
    }

    private void loadDatapackMetadata(VelvetDawn velvetDawn, Path datapackPath, String datapackId) throws Exception {
        var dataPath = datapackPath.getChild("datapack.json");
        var data = new AnyJson();
        if (dataPath.exists())
            data = dataPath.loadAsJson();

        this.world.load(velvetDawn, data);
    }

    /** Load entities into the entity map
     *
     * @param entityPath Path to the resource dir
     * @param datapackId The datapack id
     */
    private void loadEntities(VelvetDawn velvetDawn, Path entityPath, String datapackId) throws Exception {
        Map<Path, AnyJson> items = this.loadItemsInDir(entityPath, datapackId);
        for (Path path: items.keySet()) {
            var data = items.get(path);
            var entityId = this.constructId(datapackId, entityPath, path, false, data);
            System.out.println(" - " + entityId);

            // TODO extend entity data
            this.entities.put(entityId, EntityDefinition.fromJson(velvetDawn, entityId, extend(data)));
        }
    }

    /** Load tiles
     * This function will load tiles into the entities map
     *
     * @param tilesPath Path to the resource dir
     * @param datapackId The datapack id
     */
    public void loadTiles(VelvetDawn velvetDawn, Path tilesPath, String datapackId) throws Exception {
        Map<Path, AnyJson> items = this.loadItemsInDir(tilesPath, datapackId);
        for (Path path: items.keySet()) {
            var data = items.get(path);
            var tileId = this.constructId(datapackId, tilesPath, path, false, data);
            System.out.println(" - " + tileId);

            // TODO extend tile data
            this.tiles.put(tileId, TileDefinition.loadFromJson(velvetDawn, tileId, extend(data)));
        }
    }

    // TODO Test overriding
    /** Load resources into the resource map
     *
     * @param resourcesPath Path to the reosurce dir
     * @param datapackId The datapack prefix
     */
    public void loadResources(Path resourcesPath, String datapackId) throws Exception {
        AnyJson overrides = new AnyJson();

        for (Path path: resourcesPath.walk()) {
            if (path.name().equals("overrides.json"))
                overrides = path.loadAsJson();
            else {
                var resourceId = this.constructId(datapackId, resourcesPath, path, true, null);
                System.out.printf(" - %s%n", resourceId);

                String fileType = path.getFileType();
                ResourceDefinition.ResourceType type;
                switch (fileType) {
                    case "mp3":
                        type = ResourceDefinition.ResourceType.Audio;
                        break;
                    case "woff":
                        type = ResourceDefinition.ResourceType.Font;
                        break;
                    case "jpg":
                    case "png":
                    case "svg":
                        type = ResourceDefinition.ResourceType.Image;
                        break;
                    default:
                        throw new IOException(String.format(
                                "Resource '%s' is invalid. File types may only be mp3, woff, jpg, svg or png or 'overrides.json'",
                                resourceId
                        ));
                }

                // Override the resource from the overrides if it exists, otherwise, use the resource id
                if (overrides.keys().contains(resourceId))
                    resourceId = overrides.get(resourceId)
                            .validateInstanceIsString(String.format("Override values must be strings (%s)", resourceId))
                            .value;

                resources.put(resourceId, new ResourceDefinition(resourceId, path, type));
            }
        }
    }

    /** Load items from a directory.
     *
     * Abstracts entities will be added to the abstract entities dict and
     * concrete entities will be returned. Abstract entities will be assigned
     * and id here.
     *
     * @param rootPath Directly to load
     * @param datapackId: The datapack id
     * @return datapaths
     */
    public Map<Path, AnyJson> loadItemsInDir(Path rootPath, String datapackId) throws Exception {
        var dataPaths = new HashMap<Path, AnyJson>();
        for (Path path: rootPath.walk()) {
            AnyJson data = path.loadAsJson();

            var isAbstract = data.get("abstract", new AnyBool(false))
                    .validateInstanceIsBool(String.format("'abstact' key on %s must be a boolean", datapackId))
                    .toBool();
            if (isAbstract) {
                String defId = constructId(datapackId, rootPath, path, false, data);
                System.out.println(defId);
                abstractDefinitions.put(defId, data);
            } else
                dataPaths.put(path, data);
        }

        return dataPaths;
    }

    /** Construct the id for a file being loaded. If 'id' is present
     * in the file, then that will be used.
     *
     * @param datapackId The id of the datapack being loaded
     * @param loaderDirPath The root path where files are loaded from within.
     *                      This should be the path to the entities, tiles or resources
     * @param filePath Path to the file, used to construct id
     * @param includeFileType If true, the file type will be preserved
     * @param data If given, then will check to see if the file has an assigned id
     * @return New Id
     */
    public String constructId(String datapackId, Path loaderDirPath, Path filePath, boolean includeFileType, AnyJson data) throws Exception {
        if (data != null && data.containsKey("id"))
            return data.get("id")
                    .validateInstanceIsString(String.format("Id's must be a string, found in %s", filePath.toPath().toAbsolutePath())).value;

        // Get just the tokens within the loader_dir_path.
        var filePartsList = filePath.parts();
        var fileParts = filePath.parts().subList(loaderDirPath.parts().size(), filePartsList.size());

        if (!includeFileType) {
            var extension = filePath.getFileType();
            var fileName = filePath.name();
            fileParts.set(fileParts.size() - 1, fileName.substring(0, fileName.length() - extension.length() - 1));
        }

        return datapackId + ":" + String.join(".", fileParts);
    }

    /** Extend a given dictionary with the abstract definitions
     *  if the given dict has an `"extends": []` attribute
     * 
     * @param main The dict to extend
     * @return The extended json
     */
    public AnyJson extend(AnyJson main) throws Exception {
        var merged = new AnyJson();

        var extensions = main.get("extends", new AnyList())
                .validateInstanceIsList("Extends must be a list of string ID's");
    
        for (Any item: extensions.items) {
            String key = item.validateInstanceIsString("Extends must be a list of string ID's").value;
            if (!this.abstractDefinitions.containsKey(key)) 
                throw new Exception(String.format("Abstract file '%s' not found. Please mark this file with a `'abstract': true` in the file's definition.", key));

            mergeJson(merged, abstractDefinitions.get(key));
        }

        return mergeJson(merged, main);
    }

    /** Merge the two dicts without keeping a reference, allowing
     for the data to be modified in the givens dicts without updating
     the original

    @param mergeInto: Dict to copy into from `merge_from`
    @param mergeFrom: The reference dict to copy data from
    @return Combinations of the two dicts
    */
    public static AnyJson mergeJson(AnyJson mergeInto, AnyJson mergeFrom) throws Exception {
        for (String key: mergeFrom.keys()) {
            var value = mergeFrom.get(key);

            if (value instanceof AnyJson) {
                value = mergeJson(
                        (AnyJson) mergeInto
                                .get(key, new AnyJson())
                                .validateInstanceIsJson(String.format("Inconsistent data types on key '%s'", key))
                                .deepcopy(),
                        (AnyJson) value.deepcopy());
            }

            if (value instanceof AnyList) {
                var arr = new AnyList();
                arr.items.addAll(((AnyList) value.deepcopy()).items);
                arr.items.addAll(((AnyList) mergeInto
                        .get(key, Any.list())
                        .validateInstanceIsList(String.format("Inconsistent data types on key '%s'", key))
                        .deepcopy())
                        .items);

                value = arr;
            }

            mergeInto.set(key, value);
        }

        return mergeInto;
    }
}
