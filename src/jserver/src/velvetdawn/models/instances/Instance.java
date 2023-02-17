package velvetdawn.models.instances;

import velvetdawn.models.Coordinate;
import velvetdawn.models.instances.attributes.Attributes;
import velvetdawn.models.instances.tags.Tags;

public abstract class Instance {

    public final String datapackId;
    public Coordinate position;
    public final String instanceId;

    public final Attributes attributes = new Attributes();
    public final Tags tags = new Tags();

    protected Instance(String datapackId, String instanceId, Coordinate position) {
        this.datapackId = datapackId;
        this.instanceId = instanceId;
        this.position = position;
    }
}
