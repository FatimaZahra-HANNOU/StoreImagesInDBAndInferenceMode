import { createStore } from "vuex";

export default createStore({
    state: {
        selectedCarRim: {},
        selectedCarRimType: {}
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

            if (localStorage.getItem('selectedCarRimType')) {
              state.selectedCarRimType = JSON.parse(localStorage.getItem('selectedCarRimType'))
            } else {
              localStorage.setItem('selectedCarRimType', JSON.stringify(state.selectedCarRimType))
            }
        },
        clearSelectedCarRim(state) {
            state.selectedCarRim = {}
            localStorage.setItem('selectedCarRim', JSON.stringify(state.selectedCarRim))
        },
        clearSelectedCarRimType(state) {
            state.selectedCarRimType = {}
            localStorage.setItem('selectedCarRimType', JSON.stringify(state.selectedCarRimType))
        }
    },
    actions: {

    },
    modules: {

    }
})


