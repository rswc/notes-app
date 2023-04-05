<template>
    <main id="note">
        <article v-if="note">
            <div id="menu-contianer">
                <div id="menu">
                    <RouterLink to="/" class="btn-icon">
                        <Icon glyph="arrow-left" />
                    </RouterLink>
                    <button class="btn-icon" disabled>
                        <Icon glyph="lock" />
                    </button>
                    <button class="btn-icon" :disabled="note.id < 0" @click="showDelete = true;">
                        <Icon glyph="trash" />
                    </button>
                    <button class="btn-icon" :disabled="!canSave" @click="saveChanges">
                        <Icon glyph="save-floppy-disk" />
                    </button>
                </div>
            </div>

            <!-- Why span, you ask? Gaze upon this bullshit: -->
            <!-- https://stackoverflow.com/a/60482138 -->

            <span id="title" contenteditable data-placeholder="Title" @input="changes = true;" ref="titleInput">{{ note.name }}</span>

            <div id="info">
                Last edited: {{ note.last_edited }}
            </div>

            <span id="content" contenteditable data-placeholder="Take a note..." @input="changes = true;" ref="contentInput">
                {{ note.content }}
            </span>

            <NoteDeleteDialog :show="showDelete" :note="note" @close="showDelete = false;" @deleted="deleted" />
        </article>
    </main>

</template>

<script lang="ts" setup>
import { useNoteStore } from '@/stores/notes';
import type Note from '@/types/note';
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import Icon from '@/components/Icon.vue'
import router from '@/router';
import NoteDeleteDialog from '@/components/NoteDeleteDialog.vue';

const route = useRoute()
const notes = useNoteStore()

const props = defineProps<{
    create: boolean
}>()

const titleInput = ref<HTMLParagraphElement>()
const contentInput = ref<HTMLParagraphElement>()

const note = ref<Note | null>(null)

onMounted(() => {
    if (props.create) {
        note.value = {
            id: -1,
            name: '',
            content: '',
            owner: -1,
            date_created: '',
            last_edited: ''
        }
    
    } else {
        notes.details(route.params.id as string).then(v => {
            note.value = v
        })
    
    }
})

const changes = ref(false)

const canSave = computed(() => {
    return changes.value && note.value
})

const saveChanges = () => {
    changes.value = false
    
    if (note.value) {
        note.value.name = titleInput.value?.innerText || ''
        note.value.content = contentInput.value?.innerText || ''

        if (props.create) {
            notes.create(note.value).then((v: Note) => {
                // whatever
                v.content = note.value?.content
                note.value = v

                router.replace({ name: 'edit', params: { id: v.id } })
            })

        } else {
            notes.save(note.value)

        }
    }
}

const showDelete = ref(false)

const deleted = () => {
    showDelete.value = false
    router.replace('/')
}

</script>

<style>
main#note {
    padding: 24px;
    display: flex;
    justify-content: center;
}

article {
    width: 100%;
    max-width: 720px;
    padding: 20px;
    background-color: var(--color-element);
    box-shadow: 0px 1px 10px #00000026;
    border-radius: 8px;
    margin: 0 60px;
}

#content, #title {
    white-space: pre-wrap;
    outline: none;
    width: 100%;
    display: block;
}

#menu-contianer {
    position: absolute;
    left: -60px;
}

#menu {
    position: fixed;
    top: 200px;
    font-size: 1.25em;
    display: grid;
    grid-template-columns: 1fr;
    background-color: var(--color-element);
    box-shadow: 0px 1px 10px #00000026;
    padding: 8px;
    border-radius: 100vh;
    grid-gap: 16px;
}

#title {
    font-size: 3em;
    padding: 0;
    font-family: 'Playfair Display', serif;
    border-bottom: 2px solid transparent;
    word-wrap: anywhere;
    margin-bottom: 16px;
    transition: .3s border-color;
}

#title:hover {
    border-color: var(--color-border);
}

#title:focus {
    border-color: var(--color-border-hover);
}

[data-placeholder]:empty::before {
	content: attr(data-placeholder);
	font-style: italic;
	cursor: text;
	opacity: .6;
}

.btn-icon {
    line-height: 1;
    padding: 0;
    border: none;
    background: none;
    font-size: 1em;
    color: inherit;
    cursor: pointer;
    transition: .3s;
}

.btn-icon:enabled::after {
    content: " ";
    width: 0;
    height: 0;
    transition: .5s;
    position: absolute;
    top: calc(50%);
    right: calc(50%);
    opacity: .2;
    border-radius: 50%;
    background-color: currentColor;
}

.btn-icon:enabled:active::after {
    width: 36px;
    height: 36px;
    top: calc(50% - 18px);
    right: calc(50% - 18px);
    transition: .1s;
}

.btn-icon:disabled {
    cursor: not-allowed;
    opacity: 0.6;
}
</style>
