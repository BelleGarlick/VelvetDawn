import {RenderingFacade} from "../facade";

export abstract class Renderable {

    public abstract render(facade: RenderingFacade): null;
    
}
