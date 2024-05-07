<template>
  <div class="flex flex-row">
    <div class="flex flex-col w-1/2 h-full">
      <div class="ml-32 mt-4">
        <img class="object-cover" src="./components/icons/TaskMaster Logo.png" alt="TaskMaster Logo" />
      </div>
      <div id="task-form-div" class="border-transparent ml-32 mt-4">
        <form id="task-form" class="inline-flex flex-col w-full items-center" @submit.prevent="addTask">
          <label for="task-name">To-Do</label>
          <input id="task-name" type="text" v-model="newTask.title" class="mt-2 hover:outline outline-gray-200 focus:outline text-gray-600 text-center " placeholder="Task name">
          <label for="task-description" class="mt-4">Description</label>
          <textarea id="description" v-model="newTask.description" class="mt-2 hover:outline outline-gray-200 focus:outline text-gray-600 text-center" placeholder="Write a small description"> </textarea>
          <button class="bg-blue-400 hover:bg-blue-300 text-white font-bold py-2 px-4 mt-4 rounded">Add Task </button>
        </form>
      </div>
    </div>

    <div class="flex w-1/2 h-full max-h-screen overflow-y-auto ">
      <ul class="ml-24 mt-10 list-disc">
        <li id="tasks" v-for="task in tasks" :key="task.id">
          <div class="w-64 bg-blue-300 shadow-md rounded-lg p-4 mb-4 hover:bg-blue-200 transition-colors duration-300">
            <h3> {{ task.title }} </h3>
            <div class="flex overscroll-contain overflow-auto text-gray-600 max-h-20 mt-2"> {{ task.description }} </div>
            <button class="mt-5 animate-bounce"@click="completeTask(task.id)">
              <img class="w-7 h-7 rounded-full" src="./components/icons/complete.png" alt="Checkmark" />
            </button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
    data() {
      return {
        tasks: [],
        newTask: {
          id: '',
          title: '',
          description: '',
        },
        showDescription: []
      }
    },

    methods: {
      getTasks() {
        fetch('http://localhost:5000/tasks', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        })
          .then(response => { return response.json() })
          .then(data => { this.tasks = data;});
      },

      addTask() {
        fetch('http://localhost:5000/tasks', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: this.newTask.title,
            description: this.newTask.description,
          })
        })
          .then(response => { return response.json() })
          .then(data => {
            if(data.status === 'success') {
              this.newTask.id = data.id;
              this.tasks.push({
                id: data.id,
                title: this.newTask.title,
                description: this.newTask.description,
              });
              this.newTask.title = '';
              this.newTask.description = '';
            }
            else {
              alert(data.error);
            }
          });
      },

      completeTask(taskId) {
        fetch(`http://localhost:5000/tasks/${taskId}/complete`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then(response => { return response.json() })
          .then(data => {
            if(data.status === 'success') {
                this.tasks = this.tasks.filter(task => task.id !== taskId);
            }
            else {
                alert(data.error);
            }
          });
      }
    },

    mounted() {
        this.getTasks();
    }
}
</script>
