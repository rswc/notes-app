<template>
    <header>
        <h1>Notes app</h1>

		<div>
			Welcome, 
			<span style="font-weight: bold;">{{ uname }}</span>&ThickSpace;
			<a class="btn-flat negative" href="/accounts/logout/">
				<Icon glyph="log-out" />
				Log out
			</a>
		</div>
    </header>

    <RouterView />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useNoteStore } from './stores/notes';
import Icon from './components/Icon.vue';

const notes = useNoteStore()

notes.get()

const uname = window.notesapp_username

</script>

<style>
header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	position: fixed;
	top: 0;
	height: 60px;
	width: 100%;
	padding: 0 12px;
	background-color: var(--color-element);
	box-shadow: 0px 1px 10px #00000026;
	z-index: 100;
}

#app {
    min-height: 100vh;
    padding-top: 60px;
}
</style>
