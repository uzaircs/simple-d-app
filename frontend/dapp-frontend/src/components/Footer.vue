<script setup lang="ts">
import Disclaimer from './Disclaimer.vue'
</script>
<template>
    <footer class="footer">
        <div class="container">
            <Disclaimer />
        </div>
    </footer>
</template>

<style scoped>
.footer {
    padding: 16px;
    position: fixed;
    bottom: 0;
    background-color: #ddd;
    width: 100%;
    font-size: 12px;
    color: #111;

    ;
}
</style>