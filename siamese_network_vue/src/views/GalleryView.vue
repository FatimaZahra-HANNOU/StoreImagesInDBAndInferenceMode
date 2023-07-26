<template>
    <section class="container">
        <h2 class="display-6 mt-5">Gallery</h2>
        <div class="row justify-content-between">
            <div class="col-7">
                <p class="lead" v-if="displayImagesMode === ALL_MODE">
                    Total number of images: {{ carRims.length }}
                </p>
                <p class="lead" v-else>
                    Total number of types: {{ carRimsByCategory.length }}
                </p>
            </div>
            <div class="col-5 d-flex justify-content-end">
                <div class="input-group mb-3 mx-3">
                    <input
                        type="text"
                        class="form-control"
                        placeholder="Car rim type"
                        aria-label="Recipient's username"
                        aria-describedby="button-addon2"
                        v-model="searchQuery"
                        @keyup.enter="searchForCarRims"
                    >
                    <button class="btn btn-primary" type="button" id="button-addon2" @click="searchForCarRims">Search</button>
                </div>

                <div class="dropdown">
                    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Display mode
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" @click="showByCategory(false)">{{ ALL_MODE }}</a></li>
                        <li><a class="dropdown-item" @click="showByCategory(true)">{{ BY_CATEGORY_MODE }}</a></li>
                    </ul>
                </div>
            </div>
        </div>
        

        <div class="my-2">
            <div class="row" v-show="displayImagesMode === ALL_MODE">
                <div class="col-md-3 my-4" v-for="carRim in carRims" :key="carRim.id">
                    <CarRimBox :carRim="carRim" />
                </div>
            </div>
            <div class="row" v-show="displayImagesMode === BY_CATEGORY_MODE">
                <div class="col-md-3 my-4" v-for="carRimByCategory in carRimsByCategory" :key="carRimByCategory.id">
                    <CarRimTypeBox :carRimType="carRimByCategory" />
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import axios from 'axios'
    import CarRimBox from '@/components/CarRimBox.vue'
    import CarRimTypeBox from '@/components/CarRimTypeBox.vue'
    
    export default {
        name: 'GalleryView',
        components: {
            CarRimBox,
            CarRimTypeBox
        },
        data() {
            return {
                carRims: [],
                carRimsByCategory: [],
                ALL_MODE: 'All',
                BY_CATEGORY_MODE: 'By category',
                displayImagesMode: null,
                searchQuery: ''
            }
        },
        mounted() {
            document.title = 'Gallery'
            this.displayImagesMode = this.ALL_MODE;
            this.getCarRims();
            this.getCarRimsByCategory();
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
            },
            async getCarRimsByCategory() {
                await axios
                .get('/api/v1/storedCarRimTypesByCategory/')
                .then(response => {
                    this.carRimsByCategory = response.data;
                })
                .catch(error => {
                    console.log(error);
                })
            },
            showByCategory(canShowByCategory) {
                if (canShowByCategory) {
                    this.displayImagesMode = this.BY_CATEGORY_MODE;
                } else {
                    this.displayImagesMode = this.ALL_MODE;
                }
            },
            async searchForCarRims() {
                const data = JSON.stringify({
                    query: this.searchQuery
                });
                await axios
                .post('/api/v1/search/', data, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
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