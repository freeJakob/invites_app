<template>
    <v-container>
        <div v-for="user in users" :key="user.id">
            {{user}}
        </div>
    </v-container>
</template>

<script>
import { mapActions } from 'vuex';
export default {
    name: 'Map',
    data: function() {
        return {
            users: [],
            updateInterval: 10000,
        }
    },
    created: function() {
        this.getUsers();
        setInterval(this.getUsers, this.updateInterval)
        
    },
    methods: {
        ...mapActions('invitesAppModule', [
            'fetchCheckedInUsersAction'
        ]),
        getUsers: function() {
            this.fetchCheckedInUsersAction().then(resp => {
                this.users = resp;
            })
        }
    }

}
</script>