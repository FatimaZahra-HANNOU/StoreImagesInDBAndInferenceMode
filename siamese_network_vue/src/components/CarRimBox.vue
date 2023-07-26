<template>
    <router-link to="/imageDetails" @click="storeCarRim()">
        <div class="card">
            <img class="card-img-top" v-bind:src="carRim.getImage" style="cursor: pointer;">
            <div class="card-body">
                <p class="card-text">Category - {{ carRim.category }} | {{ carRim.id }}</p>
            </div>
        </div>
    </router-link>
</template>

<script>
    export default {
        name: 'CarRimBox',
        props: ['carRim'],
        components: {
        },
        data() {
            return {

            }
        },
        methods: {
            storeCarRim() {
                localStorage.setItem('selectedCarRim', JSON.stringify(this.carRim));
            }
        }
    }
</script>
