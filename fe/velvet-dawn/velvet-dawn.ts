import * as Api from "api"
import {Entity, Tile, Resource} from "models";


export class VelvetDawn {

    public static entities: { [key: string]: Entity } = {}
    public static tiles: { [key: string]: Tile } = {}
    public static resources: { [key: string]: Resource } = {}

    public static init() {
        Promise.all([
            Api.entities.getEntities().then(entities => {
                entities.forEach(entity => {
                    VelvetDawn.entities[entity.id] = entity
                })
            }),
            Api.map.getTiles().then(tiles => {
                tiles.forEach(tile => {
                    VelvetDawn.tiles[tile.id] = tile
                })
            }),
            Api.resources.getResources().then(resources => {
                resources.forEach(resource => {
                    VelvetDawn.resources[resource.id] = resource
                })
            })
        ])
            .then(() => {
                console.log(VelvetDawn.entities)
                console.log(VelvetDawn.resources)
                console.log(VelvetDawn.tiles)
                alert('Loaded')
            })
            .catch((e) => {
                console.log(e)
                alert('Unable to load')
            })
    }
}
