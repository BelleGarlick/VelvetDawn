package velvetdawn.core.players;

import velvetdawn.core.models.Team;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.core.entities.EntityInstance;

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

    public AnyJson toJson() {
        return new AnyJson()
                .set("name", this.name)
                .set("password", this.password)
                .set("admin", this.admin)
                .set("ready", this.ready)
                .set("spectating", this.spectating);
    }
}
