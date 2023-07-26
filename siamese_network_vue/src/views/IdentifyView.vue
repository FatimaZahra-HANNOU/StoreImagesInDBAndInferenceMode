<template>
    <section class="container mx-auto" style="max-width: 600px;">
        <div class="mb-3">
            <h2 class="display-6 mt-5">Identify</h2>
            <div
                v-if="showProgressBar"
                class="progress"
                role="progressbar"
                aria-label="Animated striped example"
                :aria-valuenow="progress"
                aria-valuemin="0"
                aria-valuemax="100"
            >
                <div class="progress-bar progress-bar-striped progress-bar-animated" :style="{ width: progress + '%' }"></div>
            </div>
            <label for="formFile" class="form-label col-sm-6 mt-4">Upload your image.</label>
            <input class="form-control" type="file" id="formFile" @change="handleFileUploaded">

            <div class="my-4">
                <div class="row">
                    <div class="col-6">
                        <div class="card">
                            <img v-bind:src="inputImage" class="card-img-top" style="height: 270px;" alt="...">
                            <div class="card-body">
                                <p class="card-text text-center">Input image</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="card">
                            <img v-bind:src="predictedImage" class="card-img-top" style="height: 270px;" alt="...">
                            <div class="card-body">
                                <p class="card-text text-center">Predicted Class {{ predictedClass }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <button @click="sendImageToDjango" class="btn btn-primary">Identify</button>
        </div>
    </section>


</template>

<script>
    import axios from 'axios'

    export default {
        name: 'IdentifyView',
        components: {
        },
        data() {
            return {
                inputImage: require('../assets/placeholder_image.jpg'),
                predictedImage: require('../assets/placeholder_image.jpg'),
                uploadedImage: null,
                predictedClass: null,
                progress: 0,
                showProgressBar: false,
            }
        },
        created() {
            // const socket = new WebSocket(`ws://${window.location.host}/socket/`);
            const socket = new WebSocket('ws://localhost:8000/socket/');

            socket.onopen = () => {
                socket.send(JSON.stringify({
                    message: "Hello from the client"
                }));
            }

            socket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.progress = data.progress;
            }
        },
        methods: {
            handleFileUploaded(event) {
                this.resetPredictedImage();
                const file = event.target.files[0];

                if (file) {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);

                    reader.onload = (event) => {
                        this.inputImage = event.target.result;
                        this.uploadedImage = event.target.result;
                    }

                }
            },
            sendImageToDjango() {
                this.showProgressBar = true;
                this.resetPredictedImage();

                const formData = new FormData();
                formData.append('image', this.dataURItoBlob(this.uploadedImage));

                axios
                .post('/api/v1/inference/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then(response => {
                    this.predictedClass = response.data.predictedClass;
                    this.predictedImage = response.data.predictedClassImage;
                    this.resetProgressBar();
                })
                .catch(error => {
                    console.log(error);
                });
            },
            resetPredictedImage() {
                this.predictedImage = require('../assets/placeholder_image.jpg');
                this.predictedClass = null;
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
            resetProgressBar() {
                this.showProgressBar = false;
            }
        }
    }
</script>