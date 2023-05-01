package velvetdawn.server.models;

import com.google.gson.JsonObject;
import velvetdawn.server.VelvetDawnServer;
import velvetdawn.server.VelvetDawnServerInstance;

import java.util.List;
import java.util.stream.Collectors;

public class DatapackDefinition {

    public List<JsonObject> tiles;
    public List<JsonObject> entities;
    public List<JsonObject> resources;

    public DatapackDefinition() {
        var velvetDawn = VelvetDawnServerInstance.getInstance();

        this.tiles = velvetDawn.datapacks.tiles.values()
                .stream()
                .map(item -> item.json().toGson())
                .collect(Collectors.toList());
        this.entities = velvetDawn.datapacks.entities.values()
                .stream()
                .map(item -> item.json().toGson())
                .collect(Collectors.toList());
        this.resources = velvetDawn.datapacks.resources.values()
                .stream()
                .map(item -> item.json().toGson())
                .collect(Collectors.toList());
    }

}
