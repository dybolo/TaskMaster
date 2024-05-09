<template>
    <div v-if="show" class="fixed inset-0 flex items-center justify-center">
      <div class="modal-overlay absolute inset-0 bg-gray-900 opacity-50"></div>
      <div class="modal-container bg-white w-1/3 p-8 rounded-lg shadow-lg">
        <div class="modal-header flex justify-end">
          <button @click="hideModal" class="modal-close-button">
            <button class="bg-red-400 hover:bg-red-300 text-white font-bold py-1 px-3 rounded">X</button>
          </button>
        </div>
        <div class="modal-content flex flex-col items-center">
          <h2 class="text-xl font-semibold mb-4">Error</h2>
          <p class="text-center">{{ message }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      message: String
    },
    data() {
      return {
        show: true
      };
    },
    methods: {
      hideModal() {
        this.show = false;
        this.$emit('modal-closed');
      }
    }
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    z-index: 999;
  }
  .modal-container {
    z-index: 1000;
  }
  
  
  .modal-close-button {
    background: none;
    border: none;
    cursor: pointer;
  }
  
  .modal-content {
    align-items: center; /* Centers content vertically */
  }
  
  </style>
  