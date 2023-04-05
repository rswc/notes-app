<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <svg class="icon" aria-hidden="true" focusable="false">
        <use :xlink:href="assetPath + 'icons.svg#' + glyph"></use>
    </svg>
</template>

<script setup lang="ts">
import { toRefs } from 'vue';

const props = defineProps({
    glyph: String
})

const { glyph } = toRefs(props)

const assetPath = import.meta.env.VITE_ASSETS_PATH
</script>

<style>
.icon {
    fill: currentColor;
    width: 1.5em;
    height: 1.5em;
    vertical-align: middle;
    overflow: hidden;
}
</style>
