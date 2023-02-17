import velvetdawn.models.config.Config;
import velvetdawn.VelvetDawn;

public class VelvetDawnServer {

    public static void main(String[] args) throws Exception {
        Config config = new Config();

        VelvetDawn velvetDawn = new VelvetDawn(config);
        velvetDawn.init();

//        int count = 0;
//        long start = System.currentTimeMillis();
//        for (int i = 0; i < 1_0; i++) {
//            VelvetDawn.db.tiles.setTile(0, 0, "commander:tile");
//            VelvetDawnInstance.db.tiles.getTile(0, 0);
//
//            for (int x = 0; x < 1000; x++) {
//                for (int y = 0; y < 1000; y++) {
//                    VelvetDawnInstance.db.tiles.setTile(x, y, "exampel");
//                }
//            }
//            count += VelvetDawnInstance.db.tiles.all().size();
//        }
//        long end = System.currentTimeMillis();
//
//        System.out.println((end - start) / 1000f);
//        System.out.println(count);
//        System.out.println(VelvetDawnInstance.db.);
    }
}
