package velvetdawn.models.datapacks;

import velvetdawn.utils.Path;

public class ResourceDefinition {

    public enum ResourceType {
        Audio,
        Image,
        Font
    }

    public final String resourceId;
    public final Path path;
    public final ResourceType type;

    public ResourceDefinition(String resourceId, Path path, ResourceType type) {
        this.resourceId = resourceId;
        this.path = path;
        this.type = type;
    }
}
