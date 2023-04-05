<template>
    <div class="note-card">
        <h2>{{ note.name }}</h2>
        <RouterLink class="btn-flat" :to="{ name: 'edit', params: { id: note.id } }">Edit</RouterLink>
        <a class="btn-flat">Share</a>
        <a class="btn-flat">Delete</a>
    </div>
</template>

<script lang="ts" setup>
import type Note from '@/types/note';

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
</style>
