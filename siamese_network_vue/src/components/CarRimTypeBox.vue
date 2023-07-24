<template>
    <div class="card">
        <img class="card-img-top" v-bind:src="carRimType.image">
        <div class="card-body">
            <p class="card-text">Category - {{ carRimType.category }}</p>
            <p class="card-text">Number of images {{ carRimType.count }}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'CarRimBox',
        props: ['carRimType']
    }
</script>
