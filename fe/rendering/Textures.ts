import {getResourceUrl} from "api/utils";


export class Textures {

    public static assets: { // @ts-ignore
        [key: string]: Image } = {}

    public static async load(resourcecs: string[]) {
        resourcecs.forEach(async (resourceId) => {
            Textures.loadUrl(getResourceUrl(resourceId)).then((image) => {
                Textures.assets[resourceId] = image
            });
        });
    }

    private static async loadUrl(url: string): Promise<any> {
        return new Promise(r => {
            let i = new Image();
            i.onload = (() => { r(i) });
            i.src = url;
        });
    }
}
