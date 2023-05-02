package velvetdawn.server.auth;

import io.javalin.http.Context;
import velvetdawn.core.players.Player;
import velvetdawn.server.VelvetDawnServerInstance;

public class Authenticator {

    public static Player authenticate(Context ctx) throws Exception {
        var username = ctx.header("username");
        var password = ctx.header("password");

        var player = VelvetDawnServerInstance.getInstance().players.getPlayer(username);
        if (player == null)
            throw new Exception("User does not exist");

        if (!player.password.equals(password))
            throw new Exception("Invalid authentication");

//        if host_only and not user.admin:
//        return "Host only endpoint", 401

        return player;
    }

}
