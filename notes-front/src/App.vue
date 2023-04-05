<template>
    <header>
        <h1>Notes app</h1>

        <u>Username</u>
    </header>

    <RouterView />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useNoteStore } from './stores/notes';

const notes = useNoteStore()

notes.get()

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
