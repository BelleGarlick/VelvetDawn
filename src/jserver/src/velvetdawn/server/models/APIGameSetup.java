package velvetdawn.server.models;

import lombok.Builder;
import velvetdawn.core.players.Player;
import velvetdawn.server.VelvetDawnServerInstance;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Builder
public class APIGameSetup {

    public List<String> commanders;
    public Map<String, Integer> entities;
    public boolean placedCommander;
    public Map<String, Integer> remainingEntities;

    public static APIGameSetup from(Player player) {
        var setup = VelvetDawnServerInstance.getInstance().game.setup.getSetup(player);

        return APIGameSetup.builder()
                .commanders(new ArrayList<>(setup.getCommanders()))
                .entities(setup.getEntities())
                .placedCommander(setup.isCommanderPlaced())
                .remainingEntities(setup.getRemainingEntities())
                .build();
    }
}
