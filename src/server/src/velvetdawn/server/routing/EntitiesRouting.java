package velvetdawn.server.routing;

import io.javalin.Javalin;
import velvetdawn.core.models.Coordinate;
import velvetdawn.core.models.anytype.Any;
import velvetdawn.core.models.anytype.AnyJson;
import velvetdawn.server.VelvetDawnServerInstance;
import velvetdawn.server.auth.Authenticator;
import velvetdawn.server.models.EntityUpgradeAbilitiesResponse;
import velvetdawn.server.models.GameState;

import java.util.ArrayList;
import java.util.List;

public class EntitiesRouting {

    public static void init(Javalin app) {
        app.post("/entities/move/", EntitiesRouting::moveEntity);
        app.get("/entities/available-upgrades-and-abilities/", EntitiesRouting::getEntityUpgradeAndAbilities);
        app.post("/entities/upgrade/", EntitiesRouting::performEntityUpgrade);
        app.post("/entities/ability/", EntitiesRouting::performEntityAbility);
    }

    private static void moveEntity(io.javalin.http.Context ctx) throws Exception {
        var player = Authenticator.authenticate(ctx);

        var velvetDawn = VelvetDawnServerInstance.getInstance();

        var entity = velvetDawn.entities.getById(ctx.formParam("instanceId"));

        // Parse json list
        List<Coordinate> path = new ArrayList<>();
        var rawPath = AnyJson.parse(ctx.formParam("path"));
        var items = rawPath.get("path").validateInstanceIsList("Invalid path data.");
        for (Any item: items.items) {
            path.add(Coordinate.fromJson(item.validateInstanceIsJson("Invalid coordinate item")));
        }

        VelvetDawnServerInstance.getInstance().entities.movement.move(entity, path);

        ctx.json(GameState.from(player));
    }

    private static void getEntityUpgradeAndAbilities(io.javalin.http.Context ctx) throws Exception {
        Authenticator.authenticate(ctx);

        var entity = VelvetDawnServerInstance.getInstance().entities.getById(ctx.queryParam("instanceId"));

        // Return entity update states
        ctx.json(EntityUpgradeAbilitiesResponse.from(entity));
    }

    private static void performEntityUpgrade(io.javalin.http.Context ctx) throws Exception {
        Authenticator.authenticate(ctx);

        var entity = VelvetDawnServerInstance.getInstance().entities.getById(ctx.formParam("instanceId"));

        // Perform Upgrade
        entity.upgrades.upgrade(ctx.formParam("upgradeId"));

        // Return entity update states
        ctx.json(EntityUpgradeAbilitiesResponse.from(entity));
    }

    private static void performEntityAbility(io.javalin.http.Context ctx) throws Exception {
        Authenticator.authenticate(ctx);

        var entity = VelvetDawnServerInstance.getInstance().entities.getById(ctx.formParam("instanceId"));

        // Perform Ability
        entity.abilities.perform(ctx.formParam("abilityId"));

        // Return entity update states
        ctx.json(EntityUpgradeAbilitiesResponse.from(entity));
    }
}
