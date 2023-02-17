package velvetdawn.models;


public class ActionRunnableReason {

    public final boolean isTrue;
    public final String reason;

    public ActionRunnableReason(boolean isTrue) {
        this.isTrue = isTrue;
        this.reason = "";
    }

    public ActionRunnableReason(boolean isTrue, String reason) {
        this.isTrue = isTrue;
        this.reason = reason;
    }
}
