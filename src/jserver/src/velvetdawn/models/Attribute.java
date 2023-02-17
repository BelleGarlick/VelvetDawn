package velvetdawn.models;

import com.google.gson.JsonNull;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyBool;
import velvetdawn.models.anytype.AnyFloat;
import velvetdawn.models.anytype.AnyString;

public class Attribute {

    public Long timestamp = null;

    public final String type;
    public final String instanceId;
    public final String attribute;
    public final Any value;

    public Attribute(String type, String instanceId, String attribute, Any value) {
        this.type = type;
        this.instanceId = instanceId;
        this.attribute = attribute;
        this.value = value;
    }

    public static Attribute fromJsonString(String item) {
        JsonObject jsonObject = JsonParser.parseString(item).getAsJsonObject();

        var attr = new Attribute(
                jsonObject.get("type").toString(),
                jsonObject.get("instanceId").toString(),
                jsonObject.get("attribute").toString(),
                Any.from(jsonObject.get("value").toString())
        );
        attr.timestamp = jsonObject.get("timestamp").getAsLong();

        return attr;
    }

    @Override
    public String toString() {
        JsonObject json = new JsonObject();
        json.addProperty("timestamp", this.timestamp);
        json.addProperty("type", this.type);
        json.addProperty("instanceId", this.instanceId);
        json.addProperty("attribute", this.attribute);

        json.add("value", JsonNull.INSTANCE);

        if (this.value instanceof AnyString)
            json.addProperty("value", ((AnyString) this.value).value);

        if (this.value instanceof AnyFloat)
            json.addProperty("value", ((AnyFloat) this.value).value);

        if (this.value instanceof AnyBool)
            json.addProperty("value", ((AnyBool) this.value).value);

        return json.toString();
    }
}
