<template>
    <main id="home">
		<div class="filters">
			<h1>Filter</h1>
			<div id="tag-filters">
				<template v-for="tag in notes.tags" :key="tag">
					<div @click="setFilter(tag)" :class="{'tag-filter': true, primary: filterTag === tag}">
						#{{ tag }}
					</div>
					<a class="btn-flat negative" @click="notes.deleteTag(tag)">
						<Icon glyph="trash" />
					</a>
				</template>
			</div>
		</div>
		<div id="notes">
			<div id="search-container">
				<span id="search-wrap">
					<Icon id="search-icon" glyph="search" />
					<input id="search" type="text" v-model="filterText" placeholder="Search" @change="notes.get(filterText)">
				</span>
			</div>
			<div id="create-note" class="note-card" @click="createNote">
				New note
			</div>
			<NoteCard v-for="note in filteredNotes" :note="note" :key="note.id" @delete="deleteNote = note" />
		</div>

		<NoteDeleteDialog
			:show="deleteNote !== null"
			:note="deleteNote"
			@close="deleteNote = null;"
			@deleted="deleteNote = null;" />
    </main>
</template>

<script setup lang="ts">
import NoteCard from '@/components/NoteCard.vue';
import NoteDeleteDialog from '@/components/NoteDeleteDialog.vue';
import { useNoteStore } from '@/stores/notes';
import { useRouter } from 'vue-router';
import Icon from '@/components/Icon.vue';
import { computed, ref } from 'vue';
import type Note from '@/types/note';

const notes = useNoteStore()
const router = useRouter()

const createNote = () => {
	router.push('create')
}

const filterTag = ref<string|null>(null)

const setFilter = (tag: string) => {
	if (filterTag.value === tag) {
		filterTag.value = null
	} else {
		filterTag.value = tag
	}
}

const filterText = ref('')

const filteredNotes = computed(() => {
	if (filterTag.value === null) {
		return notes.notes
	} else {
		return notes.notes.filter(v => v.tags.includes(filterTag.value!))
	}
})

const deleteNote = ref<Note|null>(null)

</script>

<style>
main#home {
	padding: 18px;
	display: flex;
}

#notes {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	grid-gap: 16px;
	width: 100%;
}

#search-container {
	grid-column: span 4;
	display: flex;
	justify-content: center;
}

#search {
	background-color: var(--color-element);
	box-shadow: 3px 3px 10px -2px #00000026;
	padding: 12px;
	border-radius: 8px;
	max-width: 512px;
	width: 100%;
	padding-left: 45px;
}

#search-wrap {
	width: 100%;
	max-width: 512px;
}

#search-icon {
	position: absolute;
	left: 7px;
	top: 7px;
	z-index: 1;
	font-size: 1.3em;
}

#create-note {
	display: flex;
	justify-content: center;
	align-items: center;
	font-size: 2em;
	font-weight: bold;
	color: var(--color-primary);
	cursor: pointer;
}

.filters {
	min-width: 140px;
	margin-right: 32px;
}

#tag-filters {
	grid-template-columns: auto min-content;
	display: grid;
	padding: 0 8px 0 4px;
	--color-mood: var(--color-text);
}

.tag-filter {
	display: flex;
	align-items: center;
	color: var(--color-mood);
	transition: .3s color;
	cursor: pointer;
}
</style>
