package velvetdawn.core.models.anytype;

import java.util.List;

public abstract class Any {

    public static AnyString from(String value) { return new AnyString(value); }
    public static AnyBool from(boolean value) { return new AnyBool(value); }
    public static AnyFloat from(float value) { return new AnyFloat(value); }
    public static AnyList from(List<Any> value) { return new AnyList(value); }
    public static AnyNull Null() { return new AnyNull(); }

    public static AnyList list() { return new AnyList(); }

    public abstract Any add(Any value);
    public abstract Any sub(Any value);
    public abstract Any mul(Any value);

    public abstract boolean equals(Any value);

    public boolean gte(Any value) { return this.toNumber() >= value.toNumber(); }
    public boolean gt(Any value) { return this.toNumber() > value.toNumber(); }
    public boolean lte(Any value) {return !this.gt(value);}
    public boolean lt(Any value) {return !this.gte(value);}

    public abstract String toString();
    public abstract float toNumber();
    public abstract boolean toBool();

    public abstract Any copy();
    public abstract Any deepcopy();

    /** Validate instance the any type, overridden in appropriate subclasses
     * Technically we can use the instanceof but this allows us to in easy line
     * cast to a type and throw and catch the error.
     */
    public AnyFloat validateInstanceIsFloat(String s) throws Exception { throw new Exception(s); }
    public AnyBool validateInstanceIsBool(String s) throws Exception { throw new Exception(s); }
    public AnyString validateInstanceIsString(String s) throws Exception { throw new Exception(s);  }
    public AnyList validateInstanceIsList(String s) throws Exception { throw new Exception(s); }
    public AnyJson validateInstanceIsJson(String s) throws Exception { throw new Exception(s); }
}
