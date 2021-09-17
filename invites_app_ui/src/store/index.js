import Vue from 'vue'
import Vuex from 'vuex'
import invitesAppModule from './invitesAppModule'

Vue.use(Vuex)

const mainStore = () => new Vuex.Store({
  modules: {
    invitesAppModule: invitesAppModule,
  }
});

export default mainStore();