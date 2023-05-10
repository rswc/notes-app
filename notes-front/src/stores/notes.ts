import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type Note from '@/types/note'
import type Tag from '@/types/tag'

const api_hostname = import.meta.env.VITE_API_HOSTNAME

export type NoteAPIResult = {success: true, note: Note} | {success: false, errors: {[key: string]: string}}

export const useNoteStore = defineStore('notes', () => {

    const _notes = ref<Note[]>([])
    const _tags = ref<string[]>([])
    const _tagIds = ref<{[key: string]: number}>({})

    const notes = computed(() => _notes.value)
    const tags = computed(() => _tags.value)

    const get = (search: string | null = null) => {
        fetch(`${api_hostname}note/${search ? "?search=" + search : ""}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })
            .then(response => response.json())
            .then(response => {
                _notes.value = response
            })
        
        fetch(`${api_hostname}tag/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })
            .then(response => response.json())
            .then(response => {
                _tags.value = response.map((v: any) => v.name)
                response.forEach((tag: Tag) => {
                    _tagIds.value[tag.name] = tag.id
                })
            })
    }

    const details = async (id: number|string) => {
        const response = await fetch(`${api_hostname}note/${id}/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        })

        return await response.json()
    }

    const save = async (note: Note): Promise<NoteAPIResult> => {
        const resp = await fetch(`${api_hostname}note/${note.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: note.name,
                content: note.content
            })
        })

        const v = await resp.json()

        if (resp.ok) {
            const idx = _notes.value.findIndex(v => v.id === note.id)

            if (idx >= 0) {
                _notes.value[idx] = v
            }

            return {
                success: true,
                note: v
            }
        }
        
        return {
            success: false,
            errors: v
        }
    }

    const create = async (note: Note): Promise<NoteAPIResult> => {
        const resp = await fetch(`${api_hostname}note/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: note.name,
                tags: note.tags,
                content: note.content
            })
        })

        const v = await resp.json()

        if (resp.ok) {
            _notes.value.push(v)

            return {
                success: true,
                note: v
            }
        }
        
        return {
            success: false,
            errors: v
        }
    }

    const remove = async (note: Note) => {
        const resp = await fetch(`${api_hostname}note/${note.id}/`, {
            method: 'DELETE',
        })

        if (resp.ok) {
            const idx = _notes.value.findIndex(v => v.id === note.id)

            if (idx >= 0) {
                _notes.value.splice(idx, 1)
            }
        }
        
        return resp.ok
    }

    const setCover = async (note: Note, image: File): Promise<NoteAPIResult> => {
        const data = new FormData()
        data.append('cover', image)

        const resp = await fetch(`${api_hostname}note/${note.id}/`, {
            method: 'PATCH',
            body: data
        })

        const v = await resp.json()

        if (resp.ok) {
            const idx = _notes.value.findIndex(v => v.id === note.id)

            if (idx >= 0) {
                _notes.value[idx] = v
            }

            return {
                success: true,
                note: v
            }
        }
        
        return {
            success: false,
            errors: v
        }
    }

    const addTag = (note: Note, tag: string) => {
        let clean = tag
        clean = clean.replace(/ /g, '-')
        clean = clean.replace(/[^\w\d+_-]/g, '')
        
        if (!clean || note.tags.includes(clean)) return
        
        note.tags.push(clean)
        _notes.value.find(v => v.id === note.id)?.tags.push(clean)

        if (!_tags.value.includes(clean)) {
            _tags.value.push(clean)
        }

        if (note.id >= 0) {
            return fetch(`${api_hostname}note/${note.id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tags: note.tags
                })
            })
        } else {
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            return new Promise(_ => {})
        }
    }

    const removeTag = (note: Note, tag: string) => {
        if (!tag) return

        const idx = note.tags.findIndex(v => v === tag)

        if (idx < 0) return

        note.tags.splice(idx, 1)

        const internal = _notes.value.find(v => v.id === note.id)
        if (internal) {
            const iidx = internal.tags.findIndex(v => v === tag)
            internal.tags.splice(iidx, 1)
        }

        if (note.id >= 0) {
            return fetch(`${api_hostname}note/${note.id}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tags: note.tags
                })
            })
        } else {
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            return new Promise(_ => {})
        }
    }

    const deleteTag = async (tag: string) => {
        if (_tagIds.value[tag]) {
            const resp = await fetch(`${api_hostname}tag/${_tagIds.value[tag]}/`, {
                method: 'DELETE',
            })

            if (resp.ok) {
                const idx = _tags.value.findIndex(v => v === tag)

                if (idx >= 0) {
                    _tags.value.splice(idx, 1)
                }
            }
            
            return resp.ok
        }
    }

    return { notes, tags, get, details, save, create, remove, setCover, addTag, removeTag, deleteTag }

})
