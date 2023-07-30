<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <router-link class="navbar-brand px-4" to="/">Car rim identifier</router-link>
        <button 
            class="navbar-toggler" 
            type="button" 
            data-toggle="collapse"
            data-target="#navbarNav" 
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
        >
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <router-link class="nav-link" to="/upload" >
                        Upload
                    </router-link>
                </li>
                <li class="nav-item active">
                    <router-link class="nav-link" to="/gallery" >
                        Gallery
                    </router-link>
                </li>
                <li class="nav-item active">
                    <router-link class="nav-link" to="/identify" >
                        Identify
                    </router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
    export default {
        name: 'NavBar',
        components: {
        }
    }
</script>
