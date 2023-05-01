package velvetdawn.server.routing;

import io.javalin.Javalin;
import io.javalin.http.Context;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.Phase;
import velvetdawn.server.VelvetDawnServerInstance;
import velvetdawn.server.auth.Authenticator;
import velvetdawn.server.models.APIGameSetup;
import velvetdawn.server.models.GameState;

public class SetupRouting {

    public static void init(Javalin app) {
        app.post("/setup/", SetupRouting::updateGameSetup);
        app.post("/setup/add/", SetupRouting::addEntityDuringSetup);
        app.post("/setup/remove/", SetupRouting::removeEntityDuringSetup);
        app.post("/setup/start-setup/", SetupRouting::startGameSetup);
    }

    private static void updateGameSetup(Context ctx) throws Exception {
        var player = Authenticator.authenticate(ctx);

        var velvetDawn = VelvetDawnServerInstance.getInstance();
        velvetDawn.game.setup.updateSetup(
                ctx.formParam("datapackId"),
                Integer.parseInt(ctx.formParam("count"))
        );

        ctx.json(APIGameSetup.from(player));
    }

    private static void addEntityDuringSetup(Context ctx) throws Exception {
        var player = Authenticator.authenticate(ctx);

        VelvetDawnServerInstance.getInstance().game.setup.placeEntity(
                player,
                ctx.formParam("datapackId"),
                new Coordinate(
                        Integer.parseInt(ctx.formParam("x")),
                        Integer.parseInt(ctx.formParam("y"))
                )
        );

        ctx.json(GameState.from(player));
    }

    private static void removeEntityDuringSetup(Context ctx) throws Exception {
        var player = Authenticator.authenticate(ctx);

        VelvetDawnServerInstance.getInstance().game.setup.removeEntity(
                player,
                new Coordinate(
                        Integer.parseInt(ctx.formParam("x")),
                        Integer.parseInt(ctx.formParam("y"))
                )
        );

        ctx.json(GameState.from(player));
    }

    private static void startGameSetup(Context ctx) throws Exception {
        var player = Authenticator.authenticate(ctx);

        var velvetDawn = VelvetDawnServerInstance.getInstance();

        if (velvetDawn.game.phase == Phase.Lobby)
            velvetDawn.game.startSetupPhase();

        ctx.json(GameState.from(player));
    }
}
