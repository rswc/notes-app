<template>
    <main id="note">
        <article v-if="note">
            <div id="menu-contianer">
                <div id="menu">
                    <RouterLink to="/" class="btn-icon">
                        <Icon glyph="arrow-left" />
                    </RouterLink>
                    <button class="btn-icon" @click="changePublic">
                        <Icon glyph="lock" v-show="!note.public" />
                        <Icon glyph="globe" v-show="note.public" />
                    </button>
                    <button class="btn-icon" :disabled="isCreating" @click="showUpload = true;">
                        <Icon glyph="media-image" />
                    </button>
                    <button class="btn-icon" :disabled="isCreating" @click="showDelete = true;">
                        <Icon glyph="trash" />
                    </button>
                    <button class="btn-icon" :disabled="!canSave" @click="saveChanges">
                        <Icon glyph="save-floppy-disk" />
                    </button>
                </div>
            </div>

            <div v-if="note.cover" id="cover" :style="{'background-image': `url(${note.cover})`}">

            </div>

            <div style="margin: 20px">
                <span class="error-text" v-for="error in validationErrors.non_field_errors" :key="error">
                    {{ error }}
                </span>
    
                <!-- Why span, you ask? -->
                <!-- https://stackoverflow.com/a/60482138 -->
                <span id="title" contenteditable data-placeholder="Title" @input="changes = true;" ref="titleInput">{{ note.name }}</span>
                <span class="error-text" v-for="error in validationErrors.name" :key="error">
                    {{ error }}
                </span>
    
                <div id="info">
                    <TagsInput :note="note" v-model="note.tags" />
                    <span v-show="!isCreating" style="text-align: right;">Last edited: {{ lastEdited }} ago</span>
                </div>
    
                <span id="content" contenteditable data-placeholder="Take a note..." @input="changes = true;" ref="contentInput">
                    {{ note.content }}
                </span>
                <span class="error-text" v-for="error in validationErrors.content" :key="error">
                    {{ error }}
                </span>
            </div>

            <NoteDeleteDialog :show="showDelete" :note="note" @close="showDelete = false;" @deleted="deleted" />
            <UploadCoverDialog :show="showUpload" :note="note" @close="showUpload = false;" @changed="changed" />
        </article>
        <Spinner v-else />
    </main>

</template>

<script lang="ts" setup>
import { useNoteStore, type NoteAPIResult } from '@/stores/notes';
import type Note from '@/types/note';
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import Icon from '@/components/Icon.vue'
import router from '@/router';
import NoteDeleteDialog from '@/components/NoteDeleteDialog.vue';
import UploadCoverDialog from '@/components/UploadCoverDialog.vue';
import { timestampFormat } from '@/util';
import Spinner from '@/components/Spinner.vue';
import TagsInput from '@/components/TagsInput.vue';


const route = useRoute()
const notes = useNoteStore()

const props = defineProps<{
    create: boolean
}>()

const titleInput = ref<HTMLParagraphElement>()
const contentInput = ref<HTMLParagraphElement>()

const note = ref<Note | null>(null)

const now = ref(Date.now())

const lastEdited = computed(() => {
    if (note.value) {
        return timestampFormat(note.value.last_edited, now.value)
    }

    return ''
})

const isCreating = computed((): boolean => {
    return !!note.value && note.value.id < 0
})

const validationErrors = ref<{[key: string]: string}>({})

onMounted(() => {
    if (props.create) {
        note.value = {
            id: -1,
            name: '',
            content: '',
            owner: -1,
            date_created: '',
            last_edited: '',
            color: 'white',
            tags: [],
            public: false
        }
    
    } else {
        notes.details(route.params.id as string).then(v => {
            note.value = v
        })
        
        setInterval(() => {
            now.value = Date.now()
        }, 60000)
        
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
            notes.create(note.value).then((res: NoteAPIResult) => {
                if (res.success) {
                    const v = res.note
                    
                    // whatever
                    v.content = note.value?.content
                    note.value = v
    
                    router.replace({ name: 'edit', params: { id: v.id } })
                } else {
                    validationErrors.value = res.errors
                }
            })

        } else {
            notes.save(note.value).then((res: NoteAPIResult) => {
                if (res.success) {
                    const v = res.note
                    
                    // whatever
                    v.content = note.value?.content
                    v.name = note.value?.name || ''
                    note.value = v

                    validationErrors.value = {}

                } else {
                    validationErrors.value = res.errors
                }
            })

        }
    }
}

const showDelete = ref(false)
const showUpload = ref(false)

const deleted = () => {
    showDelete.value = false
    router.replace('/')
}

const changed = (cover: string) => {
    note.value!.cover = cover
}

const changePublic = () => {
    notes.setPublic(note.value!, !note.value?.public).then((res: NoteAPIResult) => {
        if (res.success) {
            note.value!.public = res.note.public
        }
    })
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
    background-color: var(--color-element);
    box-shadow: 0px 1px 10px #00000026;
    border-radius: 8px;
    margin: 0 60px;
    overflow: auto;
}

#cover {
	min-height: 200px;
	background-size: cover;
	background-position-y: center;
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
    margin-bottom: 8px;
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

#info {
	display: flex;
	flex-direction: column;
	font-size: 0.9em;
	margin-bottom: 24px;
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
