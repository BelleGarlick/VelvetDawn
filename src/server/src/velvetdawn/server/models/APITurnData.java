package velvetdawn.server.models;

import velvetdawn.server.VelvetDawnServerInstance;

public class APITurnData {

    public String team;  // current team whos turn it is
    public Long start;  // The unix epoch time the turn started
    public Long seconds;  // The current length of the turn in seconds

    public APITurnData() {
        var velvetDawn = VelvetDawnServerInstance.getInstance();

        var currentTurn = velvetDawn.game.turns.getActiveTurn();
        if (currentTurn != null)
            this.team = currentTurn.teamId;

        this.start = velvetDawn.game.turns.getTurnStart();
        this.seconds = velvetDawn.game.turns.currentTurnTime();
    }
}
