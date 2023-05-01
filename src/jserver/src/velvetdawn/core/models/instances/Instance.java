package velvetdawn.core.models.instances;

import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.instances.attributes.Attributes;

import java.util.HashSet;
import java.util.Set;

public abstract class Instance {

    public String datapackId;
    public Coordinate position;
    public final String instanceId;

    public final Attributes attributes = new Attributes();
    public final Set<String> tags = new HashSet<>();

    protected Instance(String datapackId, String instanceId, Coordinate position) {
        this.datapackId = datapackId;
        this.instanceId = instanceId;
        this.position = position;
    }
}
