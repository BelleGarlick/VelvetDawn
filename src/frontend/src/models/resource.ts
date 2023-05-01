
export enum ResourceType {
    Audio = 'Audio',
    Image = 'Image',
    Font = 'Font'
}

export interface Resource {
    resourceId: string,
    resourceType: ResourceType
}
