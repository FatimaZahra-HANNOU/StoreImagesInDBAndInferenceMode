<template>
    <section class="container col-6">
        <h2 class="display-6 mt-5">Add image to category <b>{{ carRimType.category }}</b></h2>

        <div v-if="showErrorMessage">
            <div v-if="showErrorMessage" class="alert alert-danger" role="alert">
                <p class="card-text">* Please upload an image</p>
            </div>
        </div>

        <div class="row mb-3">
            <div class="col">
                <label for="formFile" class="form-label mt-4">Upload your image.</label>
                <input class="form-control" type="file" id="formFile" @change="handleFileUploaded">
            </div>
        </div>

        <div class="row mb-2">
            <div class="col">
                <div class="card">
                    <img v-bind:src="inputImage" class="card-img-top" v-bind:style="{ objectFit: fillMode }" alt="...">
                    <div class="card-body">
                        <p class="card-text text-center">{{ descriptionText }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4 mb-5">
            <div class="col">
                <button type="button" class="btn btn-success w-100" @click="saveCarRim">Save</button>
            </div>
            <div class="col">
                <button type="button" class="btn btn-danger w-100" @click="removeImageFromCard">Remove</button>
            </div>
        </div>
    </section>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'AddCarRimToCategoryView',
        components: {
        },
        data() {
            return {
                carRimType: {},
                inputImage: require('../assets/placeholder_image.jpg'),
                uploadedImage: null,
                fillMode: 'scale-down',
                showErrorMessage: false
            }
        },
        mounted() {
            document.title = 'Add image'
            this.getCarRimType();
        },
        methods: {
            getCarRimType() {
                this.carRimType = JSON.parse(localStorage.getItem('selectedCarRimType'));
            },
            handleFileUploaded(event) {
                const file = event.target.files[0];

                if (file) {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);

                    reader.onload = (event) => {
                        this.fillMode = 'contain';

                        this.inputImage = event.target.result;
                        this.uploadedImage = event.target.result;
                    }
                }
            },
            async saveCarRim() {
                if (this.uploadedImage === null) {
                    this.showErrorMessage = true;
                    return;
                } else {
                    this.showErrorMessage = false;
                }

                const formData = new FormData();
                formData.append('image', this.dataURItoBlob(this.uploadedImage));
                formData.append('category', this.carRimType.category);

                await axios
                .post('api/v1/addCarRim/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then(response => {
                    console.log(response);
                    this.$router.push({ name: 'imageGroupDetails', replace: true });
                })
                .catch(error => {
                    console.log(error);
                });
            },
            dataURItoBlob(dataURI) {
                const byteString = atob(dataURI.split(',')[1]);
                const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
                const arrayBuffer = new ArrayBuffer(byteString.length);
                const uint8Array = new Uint8Array(arrayBuffer);

                for (let i = 0; i < byteString.length; i++) {
                    uint8Array[i] = byteString.charCodeAt(i);
                }
                return new Blob([arrayBuffer], { type: mimeString });
            },
            removeImageFromCard() {
                this.fillMode = 'scale-down';

                this.inputImage = require('../assets/placeholder_image.jpg');
                this.uploadedImage = null;

                const fileInput = document.getElementById('formFile');
                fileInput.value = '';
            }
        }
    }
</script>
