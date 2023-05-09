package velvetdawn.core.models.datapacks;

import lombok.Builder;
import velvetdawn.core.utils.Path;

@Builder
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

    public String resourceId;
    public Path path;
    public ResourceType type;

    public Integer imWidth;
    public Integer imHeight;
}
