package velvetdawn.models.datapacks.tiles;

import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyNull;
import velvetdawn.models.anytype.AnyString;
import velvetdawn.utils.Json;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Set;

public class TileTextures {

    /* Tile textures data
    Tiles must have a color but also a possible assignable overlay image.
    A tile may be defined with a list of colors/images but only one will
    be chosen when the tile is created.
    */

    private static final Set<String> AvailableKeys = Set.of("color", "image", "notes");

    private List<String> colors = new ArrayList<>();
    private List<String> images = new ArrayList<>();

    /** Choose the tile colour */
    public Any chooseColor() {
        if (this.colors.isEmpty())
            return new AnyString( "#000000");

        Random rand = new Random();
        return new AnyString(this.colors.get(rand.nextInt(this.colors.size())));
    }

    /** Choose the image */
    public Any chooseImage() {
        if (images.isEmpty())
            return Any.Null();

        Random rand = new Random();
        String image = this.images.get(rand.nextInt(this.colors.size()));
        if (image.equals("null"))
            return Any.Null();

        return new AnyString(image);
    }

    /** Parse the data for load the colors and textures */
    public void load(String datapackId, Json data) throws Exception {
        this.colors = parseTexturesType(datapackId, "color", data);
        this.images = parseTexturesType(datapackId, "image", data);

        // Check for random other keys
        for (String key: data.keys()) {
            if (!AvailableKeys.contains(key))
                throw new Exception(String.format("%s textures unknown key: '%s'", datapackId, key));
        }
    }

    private List<String> parseTexturesType(String parentId, String key, Json data) throws Exception {
        if (!data.containsKey(key))
            return List.of();

        try {
            return List.of(
                    data.get(key).validateInstanceIsString("").value
            );
        } catch (Exception ignored) {}

        try {
            List<String> listValues = data.getStringList(key, List.of(), "");
            if (listValues != null)
                return listValues;
        } catch (Exception ignored) {}

        Json jsonValues = data.getJson(key, new Json(), null);
        List<String> listItems = new ArrayList<>();
        if (jsonValues != null) {
            for (String subkey: jsonValues.keys()) {
                float value = jsonValues.get(subkey).validateInstanceIsFloat(String.format("Count of %s %s must be a number in %s", key, subkey, parentId)).value;

                for (int i = 0; i < value; i++)
                    listItems.add(subkey);
            }
        }

        throw new Exception(String.format("Malformed %s tag in %s", key, parentId));
    }
}
