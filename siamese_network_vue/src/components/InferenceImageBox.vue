<template>
    <div class="card">
        <img v-bind:src="imageSrc" class="card-img-top" :height="imageHeight" v-bind:style="{ objectFit: fitMode }" alt="...">
        <div class="card-body">
            <p class="card-text text-center">{{ descriptionText }}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'InferenceImageBox',
        props: ['imageSrc', 'imageHeight', 'fitMode', 'descriptionText']
    }
</script>
