import {Renderable} from "./renderable";

export abstract class Entity extends Renderable {

    public readonly instanceId: number;
    public readonly entityId: string

    protected constructor(id: number, entityId: string) {
        super();
        this.instanceId = id;
        this.entityId = entityId;
    }
}
