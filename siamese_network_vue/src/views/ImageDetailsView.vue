<template>
    <section class="container">
        <h2 class="display-6 mt-5">Modify the selected image</h2>
        <div class="row">
            <div class="col-md-4 my-4">
                <div class="card">
                    <img class="card-img-top" v-bind:src="carRim.getImage">
                    <div class="card-body">
                        <p class="card-text text-center">Selected car rim</p>
                    </div>
                </div>
            </div>

            <div class="col-md-8 my-4 px-5">
                <div class="mb-3">
                    <label for="categoryField" class="form-label">Category</label>
                    <input 
                        type="number"
                        class="form-control"
                        id="categoryField"
                        placeholder="Insert a positive number"
                        min="0"
                        v-model="newCategory"
                    >
                </div>
                <div class="mb-3">
                    <label for="imageUrlField" class="form-label">Image URL</label>
                    <input 
                        type="text"
                        class="form-control"
                        id="imageUrlField"
                        disabled
                        v-model="carRim.getImage">
                </div>

                <div class="row mt-4">
                    <div class="col">
                        <button type="button" class="btn btn-success w-100" @click="modifyCarRim">Modify</button>
                    </div>
                    <div class="col">
                        <button type="button" class="btn btn-danger w-100" @click="deleteCarRim">Delete</button>
                    </div>
                </div>

            </div>
        </div>
    </section>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'ImageDetailsView',
        components: {
        },
        data() {
            return {
                carRim: {},
                newCategory: ''
            }
        },
        mounted() {
            document.title = 'Image details'
            this.getCarRim();
            this.newCategory = this.carRim.category;
        },
        methods: {
            getCarRim() {
                this.carRim = JSON.parse(localStorage.getItem('selectedCarRim'));
            },
            async modifyCarRim() {
                const data = JSON.stringify({
                    'id': this.carRim.id,
                    'category': this.newCategory,
                });
                await axios
                .post('/api/v1/updateCarRim/', data, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.log(error);
                });
            },
            async deleteCarRim() {
                const data = JSON.stringify({
                    'id': this.carRim.id,
                    'image': this.carRim.getImage,
                });

                await axios.post('/api/v1/deleteCarRim/', data, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then(response => {
                    console.log(response.data);
                    this.$router.push({ name: 'gallery', replace: true});
                    this.$store.commit('clearSelectedCarRim');
                })
                .catch(error => {
                    console.log(error);
                });
            }
        }
    }
</script>