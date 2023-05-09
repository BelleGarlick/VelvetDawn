package velvetdawn.server.routing;

import io.javalin.Javalin;
import io.javalin.http.Context;
import velvetdawn.server.VelvetDawnServerInstance;
import velvetdawn.server.models.datapacks.APIDatapackDefinition;

public class DatapackRouting {

    public static void init(Javalin app) {
        app.get("/datapacks/", DatapackRouting::getDatapack);
        app.get("/datapacks/<resourceId>", DatapackRouting::getResource);
    }

    private static void getDatapack(Context ctx) throws Exception {
        ctx.json(new APIDatapackDefinition());
    }

    private static void getResource(Context ctx) throws Exception {
        var resource = VelvetDawnServerInstance.getInstance().datapacks.resources.get(ctx.pathParam("resourceId"));

        if (resource == null)
            throw new Exception("File not found");

        ctx.result(resource.path.readBytes());
    }
}
