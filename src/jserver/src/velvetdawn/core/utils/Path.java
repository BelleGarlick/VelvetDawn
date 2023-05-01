package velvetdawn.core.utils;

import com.google.gson.JsonObject;
import velvetdawn.core.models.anytype.AnyJson;

import java.io.BufferedWriter;
import java.io.FileWriter;
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

    public AnyJson loadAsJson() throws Exception {
        return AnyJson.parse(this.load());
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

    public void delete() throws IOException {
        Files.delete(this.toPath());
    }

    public void rmtree() throws IOException {
        for (Path path: this.list()) {
            if (path.isDirectory())
                path.rmtree();
            else
                path.delete();
        }
    }

    public void mkdir() throws IOException {
        Files.createDirectories(this.toPath());
    }

    public void writeJson(AnyJson data) throws Exception {
        BufferedWriter writer = new BufferedWriter(new FileWriter(this.path));
        writer.write(data.toGson().toString());
        writer.close();
    }

    public void writeJson(JsonObject data) throws Exception {
        BufferedWriter writer = new BufferedWriter(new FileWriter(this.path));
        writer.write(data.toString());
        writer.close();
    }

    public String absolutePath() {
        return this.toPath().toAbsolutePath().toString();
    }

    public byte[] readBytes() throws IOException {
        return Files.readAllBytes(this.toPath());
    }

    public String readString() throws IOException {
        return Files.readString(this.toPath());
    }
}
