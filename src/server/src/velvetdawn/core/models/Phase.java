package velvetdawn.core.models;

public enum Phase {
    Lobby("lobby"),
    Setup("setup"),
    Game("game"),
    GameOver("gameOver");


    private final String text;

    Phase(final String text) {
        this.text = text;
    }

    @Override
    public String toString() {
        return text;
    }
}
