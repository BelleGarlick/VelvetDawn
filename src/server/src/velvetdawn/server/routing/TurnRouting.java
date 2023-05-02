package velvetdawn.server.routing;

import io.javalin.Javalin;
import velvetdawn.server.VelvetDawnServerInstance;
import velvetdawn.server.auth.Authenticator;
import velvetdawn.server.models.GameState;

public class TurnRouting {

    public static void init(Javalin app) {
        app.post("/turns/ready/", TurnRouting::ready);
        app.post("/turns/unready/", TurnRouting::unready);
    }

    private static void ready(io.javalin.http.Context ctx) throws Exception {
        var player = Authenticator.authenticate(ctx);

        VelvetDawnServerInstance.getInstance().game.turns.ready(player);

        ctx.json(GameState.from(player));
    }

    private static void unready(io.javalin.http.Context ctx) throws Exception {
        var player = Authenticator.authenticate(ctx);

        VelvetDawnServerInstance.getInstance().game.turns.unready(player);

        ctx.json(GameState.from(player));
    }
}
