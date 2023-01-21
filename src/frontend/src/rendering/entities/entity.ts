import {Renderable} from "./renderable";

export abstract class Entity extends Renderable {

    public readonly instanceId: string;
    public readonly entityId: string

    protected constructor(id: string, entityId: string) {
        super();
        this.instanceId = id;
        this.entityId = entityId;
    }
}
