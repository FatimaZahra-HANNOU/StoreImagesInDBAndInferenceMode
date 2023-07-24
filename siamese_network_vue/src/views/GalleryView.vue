<template>
    <section class="container">
        <h2 class="display-6 mt-5">Gallery</h2>
        <div class="row justify-content-between">
            <div class="col-8">
                <p class="lead">Total number of images: {{ carRims.length }}</p>
            </div>
            <div class="col-4 d-flex justify-content-end">
                <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Display mode
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item">Individual</a></li>
                        <li><a class="dropdown-item">By category</a></li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="my-2">
            <div class="row">
                <div class="col-md-3 my-4" v-for="carRim in carRims" :key="carRim.id">
                    <CarRimBox :carRim="carRim" />
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import axios from 'axios'
    import CarRimBox from '@/components/CarRimBox.vue'
    
    export default {
        name: 'GalleryView',
        components: {
            CarRimBox
        },
        data() {
            return {
                carRims: [],
                displayImagesMode: 'Individual'
            }
        },
        mounted() {
            this.getCarRims();
            document.title = 'Gallery'
        },
        methods: {
            async getCarRims() {
                await axios
                .get('/api/v1/storedCarRimTypes/')
                .then(response => {
                    this.carRims = response.data;
                })
                .catch(error => {
                    console.log(error);
                })
            }
        }
    }
</script>