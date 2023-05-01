package velvetdawn.core.models.datapacks;

import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.utils.Path;

public class ResourceDefinition {

    public enum ResourceType {
        Audio("Audio"),
        Image("Image"),
        Font("Font");

        private final String value;

        private ResourceType(final String value) {
            this.value = value;
        }

        @Override
        public String toString() {
            return this.value;
        }
    }

    public final String resourceId;
    public final Path path;
    public final ResourceType type;

    public ResourceDefinition(String resourceId, Path path, ResourceType type) {
        this.resourceId = resourceId;
        this.path = path;
        this.type = type;
    }

    public AnyJson json() {
        return new AnyJson()
                .set("resourceId", this.resourceId)
                .set("resourceType", this.type.toString());
    }
}
