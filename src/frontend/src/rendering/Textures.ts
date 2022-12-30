import {getResourceUrl} from "api/utils";


export class Textures {
    // @ts-ignore
    private static assets: { [key: string]: Image } = {}

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

    public static get(id: string) {
        return Textures.assets[id] ?? Textures.assets['base:textures.missing.jpg']
    }
}
