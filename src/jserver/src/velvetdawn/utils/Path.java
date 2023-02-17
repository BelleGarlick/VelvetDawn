package velvetdawn.utils;

import com.google.gson.JsonObject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Path {

    private final String path;

    public Path(String name) {
        this.path = name;
    }

    public Path getChild(String name) {
        return new Path(this.path + "/" + name);
    }

    public boolean exists() {
        return Files.exists(Paths.get(this.path));
    }

    public List<Path> list() throws IOException {
        return Files.list(Paths.get(this.path))
                .filter(path -> !path.getFileName().toString().equals(".DS_Store"))
                .map(path -> new Path(path.toAbsolutePath().toString()))
                .collect(Collectors.toList());
    }

    public boolean isDirectory() {
        return Files.isDirectory(Paths.get(this.path));
    }

    public java.nio.file.Path toPath() {
        return Paths.get(this.path);
    }

    @Override
    public String toString() {
        return this.path;
    }

    public String load() throws IOException {
        var path = Paths.get(this.path);
        return String.join("\n", Files.readAllLines(path));
    }

    public Json loadAsJson() throws IOException {
        return Json.fromString(this.load());
    }

    /** Walk directory
     *
     * Walk the tree if directories listing all files within.
     *
     * @return List of sorted paths
     */
    public List<Path> walk() throws IOException {
        if (!this.exists())
            return List.of();

        ArrayList<Path> files = new ArrayList<>();

        ArrayList<Path> unvisitedPaths = new ArrayList<>();
        unvisitedPaths.add(this);

        while (!unvisitedPaths.isEmpty()) {
            Path current = unvisitedPaths.remove(0);
            current.list().forEach(item -> {
                if (item.isDirectory())
                    unvisitedPaths.add(item);
                else
                    files.add(item);
            });
        }

        return files;
    }

    public List<String> parts() {
        var p = Paths.get(this.path).toAbsolutePath();
        ArrayList<String> parts = new ArrayList<>();
        while (p != null) {
            var fileName = p.getFileName();
            if (fileName != null)
                parts.add(0, fileName.toString());
            p = p.getParent();
        }
        return parts;
    }

    public String name() {
        return Paths.get(this.path).getFileName().toString();
    }

    public String getFileType() {
        var name = this.name();
        int i = name.lastIndexOf('.');
        if (i > 0)
            return name.substring(i + 1);
        return null;
    }

    public void saveJson(JsonObject json) {

    }
}
