package velvetdawn.mechanics.conditionals;

import velvetdawn.VelvetDawn;
import velvetdawn.mechanics.FunctionValue;
import velvetdawn.mechanics.selectors.Selector;
import velvetdawn.mechanics.selectors.Selectors;
import velvetdawn.models.anytype.Any;
import velvetdawn.models.anytype.AnyNull;
import velvetdawn.models.instances.Instance;
import velvetdawn.utils.Json;

import java.util.Map;
import java.util.Set;

public abstract class Conditional {

    // Comparison keys
    public static Map<String, Comparison> Operators = Map.of(
            "equals", Comparison.EQUALS,
            "eq", Comparison.EQUALS,
            "not-equals", Comparison.NOT_EQUALS,
            "ne", Comparison.NOT_EQUALS,
            "lt", Comparison.LESS_THAN,
            "lte", Comparison.LESS_THAN_EQUAL,
            "gt", Comparison.GREATER_THAN,
            "gte", Comparison.GREATER_THAN_EQUAL,
            "tagged", Comparison.HAS_TAG,
            "not-tagged", Comparison.NOT_HAS_TAG
    );

    // Numeric only operators
    public static Set<Comparison> NumberOnlyOperators = Set.of(
            Comparison.LESS_THAN,
            Comparison.LESS_THAN_EQUAL,
            Comparison.GREATER_THAN_EQUAL,
            Comparison.GREATER_THAN
    );

    protected Selector selector;
    public Comparison function;
    public FunctionValue functionValue;

    private final String keyword;
    private final boolean hasTagEnabled;

    public String notTrueReason = "A condition was not met.";

    /** Construct a conditional operator
     *
     * @param keyword The keyword to use for the conditional
     * @param hasTagEnabled Check if the comparison may compare tags.
     *                      This as not all conditional operations allow
     *                      you to compare against tags.
     */
    public Conditional(String keyword, boolean hasTagEnabled) {
        this.keyword = keyword;
        this.hasTagEnabled = hasTagEnabled;
    }

    public Conditional(String keyword) {
        this(keyword, true);
    }

    /** Parse the data into the conditional */
    public Conditional fromJson(VelvetDawn velvetDawn, String parentId, Json data) throws Exception {
        this.selector = Selectors.get(
                velvetDawn,
                parentId,
                data.get(this.keyword)
                                .validateInstanceIsString(String.format("Selectors must be strings (found in %s)", parentId))
                                .value);
        data.remove(this.keyword);

        data.remove("notes");

        this.notTrueReason = data.get("reason", Any.Null())
                .validateInstanceIsStringOrNull(String.format("Reason in conditional for %s must be a string", parentId))
                .toString();
        data.remove("reason");

        if (data.keys().size() != 1) {
            throw new Exception(String.format("Invalid operators in conditional: %s in %s. Conditionals must contain only one operator.", data.toString(), parentId));
        }

        for (String key: data.keys()) {
            if (!Operators.containsKey(key))
                throw new Exception(String.format("Invalid key in conditional: '%s' in %s.", key, parentId));
        }

        // Test keys
        String operatorKey = (String) data.keys().toArray()[0];
        this.function = Operators.get(operatorKey);
        this.functionValue = new FunctionValue(velvetDawn, parentId, data.get(operatorKey));

        if (NumberOnlyOperators.contains(this.function))
            this.functionValue.rawValue.validateInstanceIsFloat(String.format("Conditional in %s with operation '%s' comparison must be a float", parentId, operatorKey));

        // Can't compare tags if the condition explicitly looks to count number of items
        if (this.selector.attribute != null && (this.function == Comparison.HAS_TAG || this.function == Comparison.NOT_HAS_TAG))
            throw new Exception(String.format("Cannot compare tags on this selector with an attribute on '%s'.", parentId));
        if ((this.function == Comparison.HAS_TAG || this.function == Comparison.NOT_HAS_TAG) && !this.hasTagEnabled)
            throw new Exception(String.format("Cannot compare tags using a '{self.keyword}' comparison method on '%s'", parentId));

        return this;
    }

    /** Run the conditional function */
    public abstract boolean isTrue(Instance instance);
}
