package velvetdawn.server.models.datapacks;

import velvetdawn.server.VelvetDawnServerInstance;

import java.util.List;

public class APIDatapackDefinition {

    public List<APITileDefinition> tiles;
    public List<APIEntityDefinition> entities;
    public List<APIResourceDefinition> resources;

    public APIDatapackDefinition() {
        var velvetDawn = VelvetDawnServerInstance.getInstance();

        this.tiles = APITileDefinition.from(velvetDawn.datapacks.tiles.values());

        this.entities = APIEntityDefinition.from(velvetDawn.datapacks.entities.values());

        this.resources = APIResourceDefinition.from(velvetDawn.datapacks.resources.values());
    }

}
