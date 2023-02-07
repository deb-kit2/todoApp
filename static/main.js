const { createApp } = Vue

const TaskApp = {
    data(){
        return{
            task: "",
            tasks: [
                {title: "Eat dinner", description: "Aunty cooked dinner for us!"},
                {title: "Make App", description: "Learn about Vue."}
            ],
            message: 'My Simple To-Do'
        }
    },
    
    delimiters: ['{', '}']
}

createApp(TaskApp).mount('#app')