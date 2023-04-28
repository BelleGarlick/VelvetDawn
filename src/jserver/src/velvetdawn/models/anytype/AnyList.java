package velvetdawn.models.anytype;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonNull;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class AnyList extends Any {

    public final List<Any> items = new ArrayList<>();

    public AnyList() {}

    public AnyList(List<Any> items) {
        this.items.addAll(items);
    }

    @Override
    public Any add(Any value) {
        AnyList newList = new AnyList(this.items);
        items.add(value);

        return newList;
    }

    @Override
    public Any sub(Any value) {
        return new AnyNull();
    }

    @Override
    public Any mul(Any value) {
        return new AnyNull();
    }

    @Override
    public boolean equals(Any value) {
        if (value instanceof AnyList) {
            boolean equal = true;

            if (value.toNumber() != this.toNumber())
                return false;

            for (int i = 0; i < this.toNumber(); i++) {
                equal = this.items.get(i).equals(((AnyList) value).items.get(i));
                if (!equal)
                    break;
            }

            return equal;
        }
        return false;
    }

    @Override
    public String toString() {
        return null;
    }

    @Override
    public float toNumber() {
        return this.items.size();
    }

    @Override
    public boolean toBool() {
        return !this.items.isEmpty();
    }

    @Override
    public AnyList validateInstanceIsList(String s) {
        return this;
    }

    public int size() {
        return this.items.size();
    }

    public static AnyList of(Any ...any) {
        return new AnyList(List.of(any));
    }
    public static AnyList of(String ...any) {
        return new AnyList(
                Arrays.stream(any).map(AnyString::new).collect(Collectors.toList())
        );
    }
    public static AnyList of(List<String> items) {
        return new AnyList(
                items.stream().map(AnyString::new).collect(Collectors.toList())
        );
    }

    public Any get(int i) {
        return this.items.get(i);
    }

    public Any addAll(AnyList value) {
        this.items.addAll(value.items);
        return this;
    }

    public JsonElement toJsonElements() throws Exception {
        var array = new JsonArray();

        for (Any item: this.items) {
            if (item instanceof AnyString)
                array.add(((AnyString) item).value);
            else if (item instanceof AnyBool)
                array.add(item.toBool());
            else if (item instanceof AnyNull)
                array.add(JsonNull.INSTANCE);
            else if (item instanceof AnyFloat)
                array.add(((AnyFloat) item).value);
            else if (item instanceof AnyList)
                array.add(((AnyList) item).toJsonElements());
            else if (item instanceof AnyJson)
                array.add(((AnyJson) item).toGson());
            else {
                throw new Exception("Unknown item instance during JSON serialisation");
            }
        }

        return array;
    }

    @Override
    public Any copy() {
        var copy = new AnyList();
        copy.addAll(this);
        return copy;
    }

    @Override
    public Any deepcopy() {
        var copy = new AnyList();
        this.items.forEach(x -> copy.add(x.deepcopy()));
        return copy;
    }
}
