<template>
    <router-link to="/addCarRimToCategory">
        <div class="card">
            <img class="card-img-top" v-bind:src="image" style="cursor: pointer;">
            <div class="card-body">
                <p class="card-text text-center">{{ text }}</p>
            </div>
        </div>
    </router-link>
</template>

<script>
    export default {
        name: 'AddCarRimPlaceHolder',
        props: ['image', 'text'],
        data() {
            return {

            }
        },
    }
</script>
