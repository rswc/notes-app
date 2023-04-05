<template>
    <div class="note-card">
        <h1>{{ note.name }}</h1>
        <RouterLink class="btn-flat primary" :to="{ name: 'edit', params: { id: note.id } }">
            <Icon glyph="edit-pencil" />
            Edit
        </RouterLink>
        <a class="btn-flat primary">
            <Icon glyph="share" />
            Share
        </a>
        <a class="btn-flat negative">
            <Icon glyph="trash" />
            Delete
        </a>
    </div>
</template>

<script lang="ts" setup>
import type Note from '@/types/note';
import Icon from './Icon.vue';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps<{
    note: Note
}>()

</script>

<style>
.note-card {
	background-color: var(--color-element);
	box-shadow: 3px 3px 10px -2px #00000026;
	padding: 12px;
	border-radius: 8px;
}

.note-card h1 {
    font-size: 1.6em;
    margin-bottom: 24px;
}
</style>
