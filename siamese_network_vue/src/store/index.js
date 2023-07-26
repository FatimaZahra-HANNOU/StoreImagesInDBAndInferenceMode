import { createStore } from "vuex";

export default createStore({
    state: {
        selectedCarRim: {},
    },
    getters: {
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('selectedCarRim')) {
              state.selectedCarRim = JSON.parse(localStorage.getItem('selectedCarRim'))
            } else {
              localStorage.setItem('selectedCarRim', JSON.stringify(state.selectedCarRim))
            }
        },
        clearSelectedCarRim(state) {
            state.selectedCarRim = {}
            localStorage.setItem('selectedCarRim', JSON.stringify(state.selectedCarRim))
        }
    },
    actions: {

    },
    modules: {

    }
})


