<template>
  <div class="home">
    <keep-alive>
    <MapView></MapView>
    </keep-alive>
  </div>
</template>

<script>
// @ is an alias to /src
import MapView from '@/components/MapView.vue'

export default {
  name: 'Home',
  components: {
    MapView
  }
}
</script>
