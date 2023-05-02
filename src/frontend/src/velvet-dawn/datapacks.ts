import {Resource, ResourceType, EntityDefinition, Tile} from "models";
import * as Api from "api";
import {getResourceUrl} from "api/utils";
import {Textures} from "../rendering/Textures";
import {VelvetDawn} from "./velvet-dawn";


export class Datapacks {

    public entities: { [key: string]: EntityDefinition } = {}
    public tiles: { [key: string]: Tile } = {}
    public resources: { [key: string]: Resource } = {}

    public init() {
        return Api.datapack.getDatapacks().then(data => {
            data.entities.forEach(entity => this.entities[entity.datapackId] = entity)
            data.tiles.forEach(tile => this.tiles[tile.id] = tile)

            const imageIds: string[] = []
            data.resources.forEach(resource => {
                this.resources[resource.resourceId] = resource
                if (resource.resourceType === ResourceType.Audio) {  // Menu audio is loaded before here so it auto plays
                    VelvetDawn.audioPlayers[resource.resourceId] = new Audio(getResourceUrl(resource.resourceId));
                }
                if (resource.resourceType === ResourceType.Image)
                    imageIds.push(resource.resourceId)
            })

            Textures.load(imageIds)
        })
    }
}
