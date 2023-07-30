<template>
    <section class="container">
        <h2 class="display-6 mt-5 mb-4">Upload your images</h2>

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

        <div v-if="showSuccess" class="alert alert-success alert-dismissible fade show mt-3" role="alert">
            <strong>Success! </strong> The images were uploaded successfully to the database.
            <button @click="showSuccess = false" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>

        <div v-if="showError" class="alert alert-danger alert-dismissible fade show mt-3" role="alert">
            <strong>Error! </strong> {{ errorMessage }}
            <button @click="showError = false" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>

        <div class="row mt-3">
            <div class="col">
                <div class="card">
                    <div class="mt-3 mx-3">
                        <i class="fa-solid fa-folder-open fa-2xl"></i>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">Upload from disk</h5>
                        <p class="card-text">Select the images from your hard drive or USB, make sure to select the root folder that contains all the categories.</p>
                        <div class="row">
                            <div class="col-9">
                                <input class="form-control" type="file" id="formFile" @change="handledSelectedFiles" webkitdirectory directory multiple>
                            </div>
                            <div class="col-3 d-flex justify-content-end">
                                <a @click="sendImagesToDjango" class="btn btn-primary">Upload</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col">
                <div class="card">
                    <div class="mt-3 mx-3">
                        <i class="fa-solid fa-camera fa-2xl"></i>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">Upload from camera</h5>
                        <p class="card-text">Use the camera to take pictures of the object and store them in the database.</p>
                        <a class="btn btn-primary">Take a picture</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'UploadView',
        components: {
        },
        data() {
            return {
                data: null,

                showSuccess: false,
                showError: false,
                errorMessage: '',
                
                showProgressBar: false,
                progress: 0,
            }
        },
        mounted() {
            document.title = 'Upload images'
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
            async handledSelectedFiles(event) {
                const data = new FormData();

                const readFile = (file) => {
                    return new Promise((resolve, reject) => {
                        const reader = new FileReader();
                        reader.onload = (event) => resolve(event.target.result);
                        reader.onerror = (error) => reject(error);
                        reader.readAsArrayBuffer(file);
                    });
                };

                for (const file of event.target.files) {
                    const fileName = file.name;

                    if (fileName.endsWith('.jpg') || fileName.endsWith('.png') || fileName.endsWith('.jpeg')) {
                        try {
                            const arrayBuffer = await readFile(file);
                            const blobImage = new Blob([arrayBuffer], { type: file.type });

                            data.append('images', blobImage);
                            data.append('fileNames', fileName);
                            data.append('classNames', this.getClassName(file));

                        } catch (error) {
                            console.log('Error reading file:', error);
                        }
                    } else {
                        this.showError = true;
                        this.errorMessage = 'Please make sure to select only images with the following extensions: .jpg, .jpeg, .png';
                        this.data = null;
                        
                        return;
                    }
                }
                this.data = data;
            },
            async sendImagesToDjango() {
                if (this.data == null) {
                    this.showError = true;
                    this.errorMessage = 'No images selected, please make sure to select the root folder that contains all the images.';
                    
                    return;
                } else {
                    this.showError = false;
                    this.showProgressBar = true;
                }

                await axios
                .post('/api/v1/fillDataBase/', this.data, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'X-CSRFToken': 'csrftoken'
                    }
                })
                .then((response) => {
                    console.log(response);
                    this.showSuccess = true
                    this.progress = 0;
                    this.showProgressBar = false;
                })
                .catch((error) => {
                    console.log(error);
                    this.showError = true;
                    this.errorMessage = 'Something went wrong, please try again.';
                });
            },
            getClassName(file) {
                const filePath = file.webkitRelativePath.split('/');
                return filePath[filePath.length - 2].split('_')[1];
            },
        }
    }
</script>
