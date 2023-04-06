<template>
    <div style="display: flex;">
        <div class="tag" v-for="tag in modelValue" :key="tag">
            <div class="tag-text">
                {{ tag }}
            </div>
            <div class="remove-tag" @click="removeTag(tag)">
                <Icon glyph="plus" />
            </div>
        </div>
        <div class="tag add-tag-btn" @click.stop="setShow">
            <Icon glyph="plus" />
            <Transition name="modal">
                <div class="add-tag-container" v-show="show">
                    <form @submit.prevent="addTag(null)">
                        <input class="add-tag-input" type="text" v-model="newTag" ref="inputTag">
                    </form>
                    <div class="add-tag-option" v-for="tag in suggestions" :key="tag" @click="addTag(tag)">
                        {{ tag }}
                    </div>
                </div>
            </Transition>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue';
import Icon from '@/components/Icon.vue';
import { useNoteStore } from '@/stores/notes';
import type Note from '@/types/note';


const notes = useNoteStore()

const props = defineProps<{
    modelValue: string[],
    note: Note
}>()

const emit = defineEmits(['update:modelValue'])

const newTag = ref('')
const inputTag = ref<HTMLInputElement>()

const show = ref(false)
const setShow = () => {
    show.value = true

    setTimeout(() => {
        inputTag.value?.focus()
    }, 0)

    window.addEventListener('click', () => {
        show.value = false
    })
}

const value = computed({
    get() {
        return props.modelValue
    },
    set(value) {
        emit('update:modelValue', value)
    }
})

const suggestions = computed(() => {
    return notes.tags.filter(v => !value.value.includes(v) && (!newTag.value || v.includes(newTag.value)))
})

const addTag = (tag: string|null) => {
    const clean = tag || newTag.value

    notes.addTag(props.note, clean)

    newTag.value = ''
    show.value = false
}

const removeTag = (tag: string) => {
    notes.removeTag(props.note, tag)
}

</script>

<style>
.tag {
	margin: 2px;
	background-color: var(--color-secondary);
	line-height: 1;
	border-radius: 4px;
	display: inline-flex;
}

.tag-text {
	margin: 8px;
}

.remove-tag {
	padding: 6px;
	transition: .3s background-color;
	cursor: pointer;
}

.remove-tag .icon {
	transform: rotate(45deg);
}

.remove-tag:hover {
	background-color: var(--color-secondary-light);
}

.add-tag-btn {
    border-radius: 50%;
    transition: .3s;
    cursor: pointer;
    padding: 6px;
}

.add-tag-btn:hover {
    background-color: var(--color-secondary-light);
}

.add-tag-btn:active {
    background-color: var(--color-secondary-dark);
}

.add-tag-container {
    position: absolute;
    background-color: var(--color-element);
    box-shadow: 0px 1px 16px #00000045;
    padding: 8px 0;
    z-index: 20;
    max-width: 200px;
    word-wrap: break-word;
    top: 0;
    left: 0;
    border-radius: 6px;
    max-height: 50vh;
    overflow-y: auto;
}

.add-tag-input {
	width: 100%;
	min-width: 120px;
}

.add-tag-option {
    font-size: 1rem;
    padding: 8px 12px;
    transition: .3s background-color;
}

.add-tag-option:hover {
    background-color: var(--color-secondary-light);
}
</style>
