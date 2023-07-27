<template>
    <section class="container">
        <h2 class="display-6 mt-5">Rim category <b>{{ carRimType.category }}</b> details</h2>
        <div class="row justify-content-between">
            <div class="col-7">
                <p class="lead">Total number of images: {{ carRims.length }}</p>
            </div>

            <div class="my-2">
            <div class="row">
                <div class="col-md-3 my-4" v-for="carRim in carRims" :key="carRim.id">
                    <CarRimBox :carRim="carRim" />
                </div>
                <div class="col-md-3 my-4">
                    <AddCarRimPlaceHolder
                        :image="addImagePlaceHolder"
                        text="Add a new image"
                    />
                </div>
            </div>
        </div>
        </div>
    </section>
</template>

<script>
    import axios from 'axios';
    import CarRimBox from '@/components/CarRimBox.vue'
    import AddCarRimPlaceHolder from '@/components/AddCarRimPlaceHolder.vue';

    export default {
        name: 'ImageGroupDetailsView',
        components: {
            CarRimBox,
            AddCarRimPlaceHolder
        },
        data() {
            return {
                carRimType: {},
                carRims: [],
                addImagePlaceHolder: require('../assets/placeholder_add_image_gray.jpg')
            }
        },
        mounted() {
            document.title = 'Category details'
            this.getCarRimType();
            this.getCategoryCarRims();
        },
        methods: {
            getCarRimType() {
                this.carRimType = JSON.parse(localStorage.getItem('selectedCarRimType'));
            },
            async getCategoryCarRims() {
                const data = JSON.stringify({
                    'category': this.carRimType.category,
                });

                await axios
                .post('api/v1/getCarRimTypeImages/', data, {
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
                });
            }
        }
    }
</script>
