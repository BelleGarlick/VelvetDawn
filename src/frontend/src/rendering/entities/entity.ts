import {Renderable} from "./renderable";

export abstract class Entity extends Renderable {

    public readonly instanceId: string;
    public readonly datapackId: string

    protected constructor(id: string, datapackId: string) {
        super();
        this.instanceId = id;
        this.datapackId = datapackId;
    }
}
