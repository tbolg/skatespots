<template>
  <div id="app">
    <b-navbar toggleable="lg" type="" class="navbar-light bg-light">
      <b-navbar-brand href="/">Lockdown Skate Spots</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
         <ul class="navbar-nav mr-auto">
          <li class="nav-item">
             <router-link v-bind:class="{'active': this.$route.path == '/'}" class="nav-link" to="/">Spot Finder</router-link>
          </li>
          <li class="nav-item">
             <router-link v-bind:class="{'active': this.$route.path == '/overlapping'}" class="nav-link" to="/overlapping">Bubble Overlap Spots</router-link>
          </li>
          <li class="nav-item">
             <router-link v-bind:class="{'active': this.$route.path == '/about'}" class="nav-link" to="/about">About</router-link>
          </li>
        </ul>  
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view></router-view>
  </div>
</template>

<style>
@import 'https://bootswatch.com/4/litera/bootstrap.min.css';
@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css';
</style>
