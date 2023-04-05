<template>
    <Teleport to="body">
        <Transition name="modal">
            <div class="dialog-wrapper" v-show="props.show" @click.self="$emit('close')">
                <div class="dialog-container">
                    <h1>Delete note?</h1>
                    <div class="dialog-actions">
                        <button class="btn-pill" @click="$emit('close')">
                            Cancel
                        </button>
                        <button class="btn-pill negative" @click="remove">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<script lang="ts" setup>
import { useNoteStore } from '@/stores/notes';
import type Note from '@/types/note';

const props = defineProps<{
    show: boolean,
    note: Note
}>()

const notes = useNoteStore()

const emit = defineEmits(['close', 'deleted'])

const remove = () => {
    notes.remove(props.note).then(success => {
        if (success) {
            emit('deleted')
        }
        //TODO: Else
    })
}

</script>

<style>
.dialog-wrapper {
	position: fixed;
	z-index: 100;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
	background-color: #0003;
	display: flex;
	align-items: center;
	justify-content: center;
    transition: .3s opacity;
}

.dialog-container {
	max-width: 512px;
	background-color: var(--color-element);
	border-radius: 8px;
	padding: 24px 18px;
	width: 80%;
}

.dialog-actions {
	display: flex;
	justify-content: right;
}
</style>
