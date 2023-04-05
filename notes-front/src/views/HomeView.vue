<template>
    <main id="home">
		<div class="note-card" @click="createNote">
			Create note
		</div>
        <NoteCard v-for="note in notes.notes" :note="note" :key="note.id" />
    </main>
</template>

<script setup lang="ts">
import NoteCard from '@/components/NoteCard.vue';
import { useNoteStore } from '@/stores/notes';
import { useRouter } from 'vue-router';

const notes = useNoteStore()
const router = useRouter()

const createNote = () => {
	router.push('create')
}

</script>

<style>
main#home {
	padding: 18px;
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	grid-gap: 16px;
}
</style>
