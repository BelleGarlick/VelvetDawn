package velvetdawn.models.instances.tags;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Tags {

    private final Set<String> tags = new HashSet<>();

    public void add(String tag) {
        this.tags.add(tag);
    }

    public void addAll(List<String> tags) {
        this.tags.addAll(tags);
    }

    public void remove(String tag) {
        this.tags.remove(tag);
    }

    public boolean has(String tag) {
        return this.tags.contains(tag);
    }

    public void load(List<String> tags) {
        this.tags.addAll(tags);
    }
}
