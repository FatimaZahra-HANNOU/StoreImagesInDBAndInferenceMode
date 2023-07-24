<template>
    <div class="card">
        <img class="card-img-top" v-bind:src="carRim.getImage">
        <div class="card-body">
            <p class="card-text">Category - {{ carRim.category }} | {{ carRim.id }}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'CarRimBox',
        props: ['carRim']
    }
</script>
