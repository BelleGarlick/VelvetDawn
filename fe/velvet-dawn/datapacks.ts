import {Resource, ResourceType} from "models/resource";
import {Entity} from "models/entity";
import {Tile} from "models/tile";
import * as Api from "api/index";
import {getResourceUrl} from "api/utils";
import {Textures} from "../rendering/Textures";
import {VelvetDawn} from "./velvet-dawn";


export class Datapacks {

    public entities: { [key: string]: Entity } = {}
    public tiles: { [key: string]: Tile } = {}
    public resources: { [key: string]: Resource } = {}

    public init() {
        return Promise.all([
            Api.entities.getEntities().then(entities => {
                entities.forEach(entity => this.entities[entity.id] = entity)
            }),

            Api.map.getTiles().then(tiles => {
                tiles.forEach(tile => this.tiles[tile.id] = tile)
            }),

            Api.resources.getResources().then(resources => {
                const imageIds: string[] = []
                resources.forEach(resource => {
                    this.resources[resource.id] = resource
                    if (resource.type === ResourceType.Audio) {  // Menu audio is loaded before here so it auto plays
                        VelvetDawn.audioPlayers[resource.id] = new Audio(getResourceUrl(resource.id));
                    }
                    if (resource.type === ResourceType.Image)
                        imageIds.push(resource.id)
                })
                Textures.load(imageIds)
            })
        ])
    }
}
