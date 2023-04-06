export default interface Note {
    id: number,
    name: string,
    content?: string,
    date_created: string,
    last_edited: string,
    owner: number,
    color: string,
    tags: string[]
}