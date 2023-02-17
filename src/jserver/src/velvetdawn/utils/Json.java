package velvetdawn.utils;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import velvetdawn.models.anytype.Any;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Json {

    private final JsonObject object;

    private Json(JsonObject json) {
        this.object = json;
    }

    public Json() {
        this(new JsonObject());
    }

    public static Json fromString(String jsonData) {
        return new Json(JsonParser.parseString(jsonData).getAsJsonObject());
    }

    public Set<String> keys() {
        return object.keySet();
    }

    public boolean containsKey(String value) {
        return object.keySet().contains(value);
    }

    public List<Json> getStrictJsonList(String key, List<Json> defaultValue, String error) throws Exception {
        if (!this.containsKey(key))
            return defaultValue;

        try {
            var array = object.get(key).getAsJsonArray();

            List<Json> items = new ArrayList<>();
            for (int i = 0; i < array.size(); i++) {
                items.add(new Json(array.get(i).getAsJsonObject()));
            }
            return items;
        } catch (Exception ignored) {
            throw new Exception(error);
        }
    }

    public Json set(String id, String value) {
        this.object.addProperty(id, value);
        return this;
    }

    public Json set(String id, Boolean value) {
        this.object.addProperty(id, value);
        return this;
    }

    public Json set(String id, Integer value) {
        this.object.addProperty(id, value);
        return this;
    }

    public Json set(String id, List<Json> data) {
        var arr = new JsonArray();
        data.forEach(x -> arr.add(x.toGsonJsonElement()));
        this.object.add(id, arr);
        return this;
    }

    private JsonObject toGsonJsonElement() {
        return this.object;
    }

    public void remove(String key) {
        if (this.object.keySet().contains(key))
            this.object.remove(key);
    }

    public Any get(String name) { return this.get(name, Any.Null()); }

    public Any get(String name, Any defaultReturn) {
        if (!this.containsKey(name))
            return defaultReturn;

        var element = this.object.get(name).getAsJsonPrimitive();

        if (element.getAsJsonPrimitive().isBoolean()) {
            return Any.from(element.getAsBoolean());
        }

        if (element.getAsJsonPrimitive().isNumber()) {
            return Any.from(element.getAsFloat());
        }

        if (element.getAsJsonPrimitive().isString()) {
            return Any.from(element.getAsString());
        }

        return defaultReturn;
    }

    public Json getJson(String key, Json defaultReturn, String notJsonError) throws Exception {
        if (!this.containsKey(key))
            return defaultReturn;

        try {
            return new Json(this.object.get(key).getAsJsonObject());
        } catch (UnsupportedOperationException e) {
            throw new Exception(notJsonError);
        }
    }

    public List<String> getStringList(String key, List<String> defaultReturn, String invalidError) throws Exception {
        if (!this.containsKey(key))
            return defaultReturn;

        List<String> value = new ArrayList<String>();
        try {
            var data = this.object.getAsJsonArray(key);
            for (var item: data)
                value.add(item.getAsString());
            return value;
        } catch (UnsupportedOperationException e) {
            throw new Exception(invalidError);
        }
    }
}
