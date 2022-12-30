import {Resource, ResourceType, Entity, Tile} from "models";
import * as Api from "api";
import {getResourceUrl} from "api/utils";
import {Textures} from "../rendering/Textures";
import {VelvetDawn} from "./velvet-dawn";


export class Datapacks {

    public entities: { [key: string]: Entity } = {}
    public tiles: { [key: string]: Tile } = {}
    public resources: { [key: string]: Resource } = {}

    public init() {
        return Api.datapack.getDatapacks().then(data => {
            data.entities.forEach(entity => this.entities[entity.id] = entity)
            data.tiles.forEach(tile => this.tiles[tile.id] = tile)

            const imageIds: string[] = []
            data.resources.forEach(resource => {
                this.resources[resource.id] = resource
                if (resource.type === ResourceType.Audio) {  // Menu audio is loaded before here so it auto plays
                    VelvetDawn.audioPlayers[resource.id] = new Audio(getResourceUrl(resource.id));
                }
                if (resource.type === ResourceType.Image)
                    imageIds.push(resource.id)
            })
            Textures.load(imageIds)
        })
    }
}
