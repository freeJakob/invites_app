<template>
    <v-container>
     <v-row align-content="center" justify="center" v-if="latestArrivedUser">
        <ul>
            <div>USERNAME: {{ latestArrivedUser.name }}</div>
            <div>DISTANCE: {{ latestArrivedUser.distance }}</div>
            <div>HOURS: {{ latestArrivedUser.hours }}</div>
        </ul>
     </v-row>
    </v-container>
</template>

<script>
export default {
    name: 'Boarding',
    data: function() {
        return {
            connection: null,
            latestArrivedUser: null
        }
    },
    created: function() {
        this.connection = new WebSocket("ws://localhost/boarding/ws")

        this.connection.onmessage = (event) => {
            let jsonData = JSON.parse(event.data)
            console.log(jsonData)
            this.latestArrivedUser = jsonData;
        }
    }
}
</script>