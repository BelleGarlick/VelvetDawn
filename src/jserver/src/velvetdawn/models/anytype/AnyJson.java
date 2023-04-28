package velvetdawn.models.anytype;

import com.google.gson.JsonElement;
import com.google.gson.JsonNull;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class AnyJson extends Any {

    private final Map<String, Any> items = new HashMap<>();

    public AnyJson() {}

    public AnyJson(JsonObject json) throws Exception {
        for (String key: json.keySet())
            items.put(key, this.parseJson(json.get(key)));
    }

    public static AnyJson parse(String jsonData) throws Exception {
        return new AnyJson(JsonParser.parseString(jsonData).getAsJsonObject());
    }

    public Set<String> keys() {
        return this.items.keySet();
    }

    public boolean containsKey(String value) {
        return this.items.containsKey(value);
    }

    public AnyJson set(String id, Any value) {
        this.items.put(id, value);
        return this;
    }

    public AnyJson set(String id, String value) {
        return this.set(id, Any.from(value));
    }

    public AnyJson set(String id, float value) {
        return this.set(id, Any.from(value));
    }

    public AnyJson set(String id, Boolean value) {
        return this.set(id, Any.from(value));
    }

    public AnyJson set(String id, Integer value) {
        return this.set(id, Any.from(value));
    }

    public void remove(String key) {
        if (this.containsKey(key))
            this.items.remove(key);
    }

    public Any get(String name) { return this.get(name, null); }

    public Any get(String name, Any defaultReturn) {
        if (!this.containsKey(name))
            return defaultReturn;

        return this.items.get(name);
    }

    private Any parseJson(JsonElement item) throws Exception {
        if (item.isJsonNull())
            return Any.Null();

        try {
            var element = item.getAsJsonPrimitive();
            if (element.getAsJsonPrimitive().isBoolean()) {
                return Any.from(element.getAsBoolean());
            }

            if (element.getAsJsonPrimitive().isNumber()) {
                return Any.from(element.getAsFloat());
            }

            if (element.getAsJsonPrimitive().isString()) {
                return Any.from(element.getAsString());
            }
        } catch (Exception ignored) {}

        try {
            var items = item.getAsJsonArray();
            var list = new AnyList();
            for (int i = 0; i < items.size(); i++) {
                list.items.add(parseJson(items.get(i)));
            }
            return list;
        } catch (Exception ignored) {}

        try {
            var object = item.getAsJsonObject();
            var json = new AnyJson();
            for (String key: object.keySet()) {
                json.set(key, parseJson(object.get(key)));
            }
            return json;
        } catch (Exception ignored) {}

        throw new Exception("Unable to parse json element");
    }

    @Override
    public Any add(Any value) {
        return Any.Null();
    }

    @Override
    public Any sub(Any value) {
        return Any.Null();
    }

    @Override
    public Any mul(Any value) {
        return Any.Null();
    }

    @Override
    public boolean equals(Any value) {
        return false;
    }

    @Override
    public String toString() {
        try {
            return this.toGson().toString();
        } catch (Exception e) {
            return null;
        }
    }

    @Override
    public float toNumber() {
        return this.keys().size();
    }

    @Override
    public boolean toBool() {
        return !this.keys().isEmpty();
    }

    @Override
    public AnyJson validateInstanceIsJson(String s) {
        return this;
    }

    public JsonObject toGson() throws Exception {
        JsonObject json = new JsonObject();

        for (String key: this.keys()) {
            Any item = this.get(key);

            if (item instanceof AnyString)
                json.addProperty(key, ((AnyString) item).value);
            else if (item instanceof AnyBool)
                json.addProperty(key, item.toBool());
            else if (item instanceof AnyNull)
                json.add(key, JsonNull.INSTANCE);
            else if (item instanceof AnyFloat)
                json.addProperty(key, ((AnyFloat) item).value);
            else if (item instanceof AnyList)
                json.add(key, ((AnyList) item).toJsonElements());
            else if (item instanceof AnyJson)
                json.add(key, ((AnyJson) item).toGson());
            else {
                throw new Exception("Unknown item instance during JSON serialisation");
            }
        }
        return json;
    }

    @Override
    public Any copy() {
        var copy = new AnyJson();
        this.keys().forEach(key -> copy.set(key, this.get(key)));
        return copy;
    }

    @Override
    public Any deepcopy() {
        var copy = new AnyJson();
        this.keys().forEach(key -> copy.set(key, this.get(key).deepcopy()));
        return copy;
    }
}
