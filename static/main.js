const { createApp } = Vue

const TaskApp = {
    data(){
        return{
            task: {
                "title" : "",
                "description" : ""
            },
            tasks: [],
            message: 'simple To-Do App'
        }
    },

    async created(){
        await this.getTasks()
    },

    methods: {
        async getTasks(){
            const response = await fetch(window.location, {
                method: "get",
                headers: {
                    "X-Requested-With" : "XMLHttpRequest"
                }
            }) 

            this.tasks = await response.json()
        },

        async createTask(){
            await this.getTasks()

            const response = await fetch(window.location + "create", {
                method: "post",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With" : "XMLHttpRequest"
                },
                body: JSON.stringify(this.task)
            })

            await this.getTasks()
        }
    },

    delimiters: ['{', '}']
}

createApp(TaskApp).mount('#app')