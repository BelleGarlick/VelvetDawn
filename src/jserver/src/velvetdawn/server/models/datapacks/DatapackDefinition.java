package velvetdawn.server.models.datapacks;

import com.google.gson.JsonObject;
import velvetdawn.server.VelvetDawnServerInstance;

import java.util.List;
import java.util.stream.Collectors;

public class DatapackDefinition {

    public List<JsonObject> tiles;
    public List<APIEntityDefinition> entities;
    public List<JsonObject> resources;

    public DatapackDefinition() {
        var velvetDawn = VelvetDawnServerInstance.getInstance();

        this.tiles = velvetDawn.datapacks.tiles.values()
                .stream()
                .map(item -> item.json().toGson())
                .collect(Collectors.toList());

        this.entities = APIEntityDefinition.from(velvetDawn.datapacks.entities.values());

        this.resources = velvetDawn.datapacks.resources.values()
                .stream()
                .map(item -> item.json().toGson())
                .collect(Collectors.toList());
    }

}
