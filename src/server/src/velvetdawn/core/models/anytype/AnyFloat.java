package velvetdawn.core.models.anytype;

public class AnyFloat extends Any {

    public final float value;

    public AnyFloat(float value) {
        this.value = value;
    }

    @Override
    public float toNumber() {
        return value;
    }

    @Override
    public boolean toBool() { return this.value != 0; }

    @Override
    public Any add(Any value) {
        if (value instanceof AnyFloat)
            return new AnyFloat(this.toNumber() + ((AnyFloat) value).value);

        return Any.Null();
    }

    @Override
    public Any sub(Any value) {
        if (value instanceof AnyFloat)
            return new AnyFloat(this.toNumber() - ((AnyFloat) value).value);

        return Any.Null();
    }

    @Override
    public Any mul(Any value) {
        if (value instanceof AnyFloat)
            return new AnyFloat(this.toNumber() * ((AnyFloat) value).value);

        return Any.Null();
    }

    @Override
    public String toString() {
        return Float.toString(this.value);
    }

    @Override
    public boolean equals(Any value) {
        if (value instanceof AnyFloat)
            return this.value == ((AnyFloat) value).value;
        return false;
    }

    @Override
    public AnyFloat validateInstanceIsFloat(String s) throws Exception {
        return this;
    }

    public AnyFloat validateMinimum(float minValue, String s) throws Exception {
        if (this.value < minValue)
            throw new Exception(s);
        return this;
    }

    @Override
    public Any copy() {
        return new AnyFloat(this.value);
    }

    @Override
    public Any deepcopy() {
        return this.copy();
    }
}
