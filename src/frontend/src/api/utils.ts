import axios from "axios";
import { inDevMove } from "../constants";


export function getUrl() {
    if (inDevMove())
        return "http://localhost:1642/"

    return window.location.href
}


export function getResourceUrl(resourceId: string) {
    return `${getUrl()}/datapacks/${resourceId}`
}


export function get(path: string, data?: { [key: string]: any }): Promise<any> {
    return axios.get(getUrl() + path, data).then(x => x.data)
}


export function post(path: string, data: { [key: string]: any }): Promise<any> {
    return axios.post(
        getUrl() + path,
        data,
        { headers: { "Content-Type": "multipart/form-data" }}
    ).then(x => x.data)
}
