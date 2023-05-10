<template>
    <Teleport to="body">
        <Transition name="modal">
            <div class="dialog-wrapper" v-show="props.show" @click.self="$emit('close')">
                <div class="dialog-container">
                    <h1>Upload cover image</h1>
                    <input type="file" ref="imageInput">
                    <div class="error-text" v-show="error">
                        An error occurred. Please try again later.
                    </div>
                    <div class="dialog-actions">
                        <button class="btn-pill" @click="$emit('close')">
                            Cancel
                        </button>
                        <button class="btn-pill primary" @click="submit">
                            Save
                        </button>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script lang="ts" setup>
import type { NoteAPIResult } from '@/stores/notes';
import { useNoteStore } from '@/stores/notes';
import type Note from '@/types/note';
import { ref } from 'vue';

const props = defineProps<{
    show: boolean,
    note: Note
}>()

const notes = useNoteStore()

const emit = defineEmits(['close', 'changed'])

const imageInput = ref<HTMLInputElement>()
const error = ref(false)

const submit = () => {
    const img = imageInput.value?.files
    if (img && img[0]) {
        error.value = false

        notes.setCover(props.note, img[0]).then((res: NoteAPIResult) => {
            if (res.success) {
                emit('changed', res.note.cover)
                emit('close')
            } else {
                error.value = true
            }
        })
    }
}

</script>