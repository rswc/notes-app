import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type Note from '@/types/note'

const api_hostname = import.meta.env.VITE_API_HOSTNAME

export const useNoteStore = defineStore('notes', () => {

    const _notes = ref<Note[]>([])
    const _tags = ref<string[]>([])

    const notes = computed(() => _notes.value)
    const tags = computed(() => _tags.value)

    const get = () => {
        fetch(`${api_hostname}note/`, {
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

    const save = (note: Note) => {
        return fetch(`${api_hostname}note/${note.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: note.name,
                content: note.content
            })
        })
    }

    const create = async (note: Note) => {
        const resp = await fetch(`${api_hostname}note/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: note.name,
                content: note.content
            })
        })

        const v = await resp.json()

        _notes.value.push(v)
        
        return v
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

    const addTag = (note: Note, tag: string) => {
        let clean = tag
        clean = clean.replace(/ /g, '-')
        clean = clean.replace(/[^\w\d+_-]/g, '')
        
        if (!clean || note.tags.includes(clean)) return
        
        note.tags.push(clean)

        if (!_tags.value.includes(clean)) {
            _tags.value.push(clean)
        }

        return fetch(`${api_hostname}note/${note.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tags: note.tags
            })
        })
    }

    const removeTag = (note: Note, tag: string) => {
        if (!tag) return

        const idx = note.tags.findIndex(v => v === tag)

        if (idx < 0) return

        note.tags.splice(idx, 1)

        return fetch(`${api_hostname}note/${note.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tags: note.tags
            })
        })
    }

    return { notes, tags, get, details, save, create, remove, addTag, removeTag }

})
