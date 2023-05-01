package velvetdawn.server.models;

import com.google.gson.JsonElement;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyList;
import velvetdawn.server.VelvetDawnServerInstance;

public class MapResponse {

    public JsonElement tiles;

    public MapResponse() {
        var tiles = VelvetDawnServerInstance.getInstance().map.getTiles();

        var tileIds = new AnyList();
        tiles.forEach(items -> {
            var row = new AnyList();
            items.forEach(item -> row.add(Any.from(item.datapackId)));
            tileIds.add(row);
        });

        this.tiles = tileIds.toJsonElements();
    }

}
