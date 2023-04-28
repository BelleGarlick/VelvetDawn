package velvetdawn.models;

import java.util.Objects;

public class Coordinate {

    public final float x;
    public final float y;

    public Coordinate() {
        this(0, 0);
    }

    public Coordinate(float x, float y) {
        this.x = x;
        this.y = y;
    }

    public int tileX() {
        return (int) Math.floor(x);
    }

    public int tileY() {
        return (int) Math.floor(y);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Coordinate that = (Coordinate) o;
        return Float.compare(that.x, x) == 0 && Float.compare(that.y, y) == 0;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    public Coordinate up() {
        return new Coordinate(this.x, this.y - 1);
    }
    public Coordinate down() {
        return new Coordinate(this.x, this.y + 1);
    }
    public Coordinate left() {
        return new Coordinate(this.x - 1, this.y);
    }
    public Coordinate right() {
        return new Coordinate(this.x + 1, this.y);
    }

    public boolean tileEquals(Coordinate coordinate) {
        return this.tileX() == coordinate.tileX() && this.tileY() == coordinate.tileY();
    }
}
