import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type Note from '@/types/note'

const api_hostname = import.meta.env.VITE_API_HOSTNAME

export const useNoteStore = defineStore('notes', () => {

    const _notes = ref<Note[]>([])

    const notes = computed(() => _notes.value)

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

            if (idx) {
                _notes.value.splice(idx)
            }
        }
        
        return resp.ok
    }

    return { notes, get, details, save, create, remove }

})
