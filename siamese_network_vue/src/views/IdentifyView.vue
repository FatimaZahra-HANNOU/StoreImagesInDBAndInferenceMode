<template>
    <section class="container mx-auto">
        <div class="mb-3">
            <h2 class="display-6 mt-5">Identify</h2>

            <div v-if="showErrorMessage">
                <div v-if="showErrorMessage" class="alert alert-danger" role="alert">
                    <p class="card-text" v-for="error in errors" :key="error" >* {{ error }}</p>
                </div>
            </div>

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

            <div class="row">
                <div class="col-4">
                    <label for="formFile" class="form-label mt-4">Upload your image.</label>
                    <input class="form-control" type="file" id="formFile" @change="handleFileUploaded">
                </div>

                <div class="col-4">
                    <label for="modelSelector" class="form-label mt-4">Select your model.</label>
                    <div class="dropdown">
                        <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                            {{ modelName }}
                        </button>
                        <ul class="dropdown-menu">
                            <li v-for="model in models" :key="model">
                                <a class="dropdown-item" @click="changeModelName(model)">{{ model }}</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="row my-4">
                <div class="col-4">
                    <InferenceImageBox
                        :imageSrc="inputImage"
                        :imageHeight="imageHeight"
                        :fitMode="fitModeInput"
                        :descriptionText="'Input image'"
                        :footerBackgroundColor="'bg-transparent'"
                    />
                </div>

                <div class="col-4">
                    <InferenceImageBox
                        :imageSrc="predictedImage"
                        :imageHeight="imageHeight"
                        :fitMode="fitModePrediction"
                        :descriptionText="'Predicted class - ' + predictedClass"
                        :footerBackgroundColor="'bg-transparent'"
                    />
                </div>
            </div>

            <button @click="sendImageToDjango" class="btn btn-primary">Identify</button>

            <div class="row" v-if="topNPredictions.length">
                <h2 class="display-6 mt-5 mb-4">Top 3 predictions</h2>

                <div class="col-4" v-for="(prediction, index) in topNPredictions" :key="prediction">
                    <InferenceImageBox
                        :imageSrc="prediction[1]"
                        :imageHeight="imageHeight"
                        :fitMode="fitModePrediction"
                        :descriptionText="'Predicion N° ' + (index+1) + ' | ' + prediction[0]"
                        :footerBackgroundColor="topNCardBackgroundColor[index]"
                    />
                </div>
            </div>

        </div>
    </section>


</template>

<script>
    import axios from 'axios'
    import InferenceImageBox from '@/components/InferenceImageBox.vue';

    export default {
        name: 'IdentifyView',
        components: {
            InferenceImageBox
        },
        data() {
            return {
                inputImage: require('../assets/placeholder_image.jpg'),
                predictedImage: require('../assets/placeholder_image.jpg'),
                uploadedImage: null,

                modelName: 'Nothing selected',
                models: [],

                predictedClass: '',
                topNPredictions: [],

                progress: 0,
                showProgressBar: false,

                imageHeight: 350,
                fitModeInput: 'scale-down',
                fitModePrediction: 'scale-down',
                
                showErrorMessage: false,
                errors: [],

                topNCardBackgroundColor: ['bg-success', 'bg-warning', 'bg-danger']
            }
        },
        mounted() {
            document.title = 'Identify'
            this.getListOfModels();
        },
        created() {
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
            async getListOfModels() {
                await axios
                .get('/api/v1/models/')
                .then(response => {
                    this.models = response.data['models'];
                })
                .catch(error => {
                    console.log(error);
                });
            },
            handleFileUploaded(event) {
                this.resetPredictedImage();
                const file = event.target.files[0];

                if (file) {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);

                    reader.onload = (event) => {
                        this.fitModeInput = 'cover';
                        this.inputImage = event.target.result;
                        this.uploadedImage = event.target.result;
                    }

                }
            },
            sendImageToDjango() {
                this.errors = [];
                if (this.errorsExist()) {
                    return;
                }

                this.showProgressBar = true;
                this.resetPredictedImage();

                const formData = new FormData();
                const imageBlob = this.dataURItoBlob(this.uploadedImage)

                formData.append('image', imageBlob);
                formData.append('model', this.modelName);

                axios
                .post('/api/v1/inference/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then(response => {
                    this.fitModePrediction = 'fill';

                    this.predictedClass = response.data.predictedClass;
                    this.predictedImage = response.data.predictedClassImage;
                    this.topNPredictions = response.data.topNPredictions;

                    this.resetProgressBar();
                })
                .catch(error => {
                    console.log(error);
                });
            },
            errorsExist() {
                if (this.modelName === 'Nothing selected') {
                    this.errors.push('Please select a model.');
                }

                if (this.uploadedImage == null) {
                    this.errors.push('Please upload an image.');
                }

                if (this.errors.length > 0) {
                    this.showErrorMessage = true;
                    return true;
                } else {
                    this.showErrorMessage = false;
                    return false;
                }
            },
            resetPredictedImage() {
                this.predictedImage = require('../assets/placeholder_image.jpg');
                this.predictedClass = '';
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
                this.progress = 0;
            },
            changeModelName(modelName) {
                this.modelName = modelName;
            }
        }
    }
</script>
