package velvetdawn.server.routing;

import io.javalin.Javalin;
import velvetdawn.core.models.Coordinate;
import velvetdawn.server.VelvetDawnServerInstance;
import velvetdawn.server.auth.Authenticator;
import velvetdawn.server.models.GameState;

public class CombatRouting {

    public static void init(Javalin app) {
        app.post("/combat/attack", CombatRouting::attackEntity);
    }

    private static void attackEntity(io.javalin.http.Context ctx) throws Exception {
        var player = Authenticator.authenticate(ctx);

        var entity = VelvetDawnServerInstance.getInstance()
                .entities
                .getById(ctx.formParam("instanceId"));

        var position = new Coordinate(
                Integer.parseInt(ctx.formParam("x")),
                Integer.parseInt(ctx.formParam("y"))
        );

        entity.combat.attack(position);

        ctx.json(GameState.from(player));
    }
}
