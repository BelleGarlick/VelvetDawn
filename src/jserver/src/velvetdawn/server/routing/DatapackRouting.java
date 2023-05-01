package velvetdawn.server.routing;

import io.javalin.Javalin;
import io.javalin.http.Context;
import velvetdawn.server.VelvetDawnServerInstance;
import velvetdawn.server.models.DatapackDefinition;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DatapackRouting {

    private static Logger logger = LoggerFactory.getLogger(DatapackRouting.class);

    public static void init(Javalin app) {
        app.get("/datapacks/", DatapackRouting::getDatapack);
        app.get("/datapacks/<resourceId>", DatapackRouting::getResource);
    }

    private static void getDatapack(Context ctx) throws Exception {

        ctx.json(new DatapackDefinition());
    }

    private static void getResource(Context ctx) throws Exception {
        VelvetDawnServerInstance.getInstance().datapacks.resources.keySet().forEach(key -> {
            logger.info(key);
        });
        var resource = VelvetDawnServerInstance.getInstance().datapacks.resources.get(ctx.pathParam("resourceId"));
//        logger.info(resource);
        logger.debug("Debug log message");
        logger.info("Info log message");
        logger.error("Error log message");

        if (resource == null)
            throw new Exception("File not found");

        ctx.result(resource.path.readBytes());
    }
}
