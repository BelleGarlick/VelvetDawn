package velvetdawn.players;

import com.google.gson.JsonObject;
import velvetdawn.models.Team;
import velvetdawn.models.anytype.AnyJson;
import velvetdawn.models.instances.entities.EntityInstance;

import java.util.HashSet;
import java.util.Set;

public class Player {

    public final String name;
    public final String password;
    public final boolean admin;

    public boolean ready = false;
    public boolean spectating = false;

    public Team team = null;

    public Set<EntityInstance> entities = new HashSet<>();

    public Player(String name, String password, boolean admin) {
        this.name = name;
        this.password = password;
        this.admin = admin;
    }

    public static Player fromJson(AnyJson playerJson) throws Exception {
        var player = new Player(
                playerJson.get("name").validateInstanceIsString("Invalid player save. Player names must be strings.").value,
                playerJson.get("password").validateInstanceIsString("Invalid player save. Player passwords must be strings.").value,
                playerJson.containsKey("admin") && playerJson.get("admin").validateInstanceIsBool("Invalid player save. Player admin must be a bool").toBool()
        );

        return player;
    }

    public JsonObject toJson() {
        JsonObject json = new JsonObject();
        json.addProperty("name", this.name);
        json.addProperty("password", this.password);
        json.addProperty("admin", this.admin);
        json.addProperty("ready", this.ready);
        json.addProperty("spectating", this.spectating);

        return json;
    }
}
