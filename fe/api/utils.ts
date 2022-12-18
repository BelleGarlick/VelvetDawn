import axios from "axios";


export function getUrl() {
    let port = window.location.port
    port = '666'
    return window.location.protocol + "//" + window.location.hostname + ":" + 666
}


export function getResourceUrl(resourceId: string) {
    return `${getUrl()}/resources/${resourceId}`
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
