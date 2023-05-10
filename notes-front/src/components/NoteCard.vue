<template>
    <div class="note-card">
        <div>
            <div class="note-card-cover" :style="{'background-image': `url(${note.cover})`}" >
                <h1>{{ note.name }}</h1>
            </div>
        </div>
        <div style="padding: 12px;">
            <span v-for="tag in note.tags" :key="tag" class="mini-tag">#{{ tag }}</span>
        </div>
        <div style="padding: 12px;">
            <RouterLink class="btn-flat primary" :to="{ name: 'edit', params: { id: note.id } }">
                <Icon glyph="edit-pencil" />
                Edit
            </RouterLink>
            <a class="btn-flat primary">
                <Icon glyph="share" />
                Share
            </a>
            <a class="btn-flat negative" @click="emit('delete')">
                <Icon glyph="trash" />
                Delete
            </a>
        </div>
    </div>
</template>

<script lang="ts" setup>
import type Note from '@/types/note';
import Icon from './Icon.vue';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const props = defineProps<{
    note: Note
}>()

const emit = defineEmits(['delete'])

</script>

<style>
.note-card {
	background-color: var(--color-element);
	box-shadow: 3px 3px 10px -2px #00000026;
	border-radius: 8px;
	display: flex;
	flex-direction: column;
	justify-content: space-between;
    overflow: auto;
}

.note-card-cover {
	min-height: 100px;
	background-size: cover;
	background-position-y: center;
    padding: 12px;
}

.note-card h1 {
	font-size: 1.6em;
	margin-bottom: 24px;
	display: inline;
	background-color: var(--color-element);
	padding: 0.2rem;
}

.mini-tag {
    margin: 0 4px;
    opacity: 0.8;
}
</style>
