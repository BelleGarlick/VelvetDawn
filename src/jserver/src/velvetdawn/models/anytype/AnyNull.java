package velvetdawn.models.anytype;

public class AnyNull extends AnyFloat {

    public AnyNull() {
        super(0);
    }

    @Override
    public String toSaveString() {
        return "n#";
    }

    @Override
    public String toString() {
        return null;
    }

    @Override
    public AnyFloat validateInstanceIsFloat(String s) throws Exception {
        throw new Exception(s);
    }

    @Override
    public Any validateInstanceIsStringOrNull(String s) {return this;}
}
