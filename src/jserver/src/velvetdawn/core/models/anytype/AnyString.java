package velvetdawn.core.models.anytype;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class AnyString extends Any {

    public final String value;

    public AnyString(String value) {
        this.value = value;
    }

    @Override
    public Any add(Any value) {
        if (value instanceof AnyString)
            return new AnyString(this.value + ((AnyString) value).value);
        return Any.Null();
    }

    @Override
    public Any sub(Any value) {
        return Any.Null();
    }

    @Override
    public Any mul(Any value) {
        return Any.Null();
    }

    @Override
    public String toString() {
        return this.value;
    }

    @Override
    public float toNumber() {
        return this.value.length();
    }

    @Override
    public boolean toBool() {
        return this.value.length() > 0;
    }

    @Override
    public boolean equals(Any value) {
        if (value instanceof AnyString)
            return this.value.equals(((AnyString) value).value);
        return false;
    }

    @Override
    public AnyString validateInstanceIsString(String s) {
        return this;
    }

    public AnyString validateRegex(String regex, String error) throws Exception {
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(this.value);
        if (!matcher.find()) {
            throw new Exception("Names must be 3-8 characters long and letters & numbers only");
        }

        return this;
    }

    @Override
    public Any copy() {
        return new AnyString(this.value);
    }

    @Override
    public Any deepcopy() {
        return this.copy();
    }

    public AnyFloat castToFloat() {
        return new AnyFloat(Float.parseFloat(this.value));
    }
}
