
export enum ResourceType {
    Audio = 'audio',
    Image = 'image',
    Font = 'font'
}

export interface Resource {
    id: string,
    type: ResourceType
}
