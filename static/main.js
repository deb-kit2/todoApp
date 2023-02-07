const { createApp } = Vue

const TaskApp = {
    data(){
        return{
            task: {
                "_id" : "",
                "title" : "",
                "description" : "",
                "status" : ""
            },
            tasks: [],
            message: 'simple To-Do App'
        }
    },

    async created(){
        await this.getTasks()
    },

    methods: {
        async sendReqest(url, method, data){
            const myHeaders = new Headers({
                "Content-Type": "application/json",
                "X-Requested-With" : "XMLHttpRequest"
            })

            const response = await fetch(url, {
                method: method,
                headers: myHeaders,
                body: data
            })

            return response
        },

        async getTasks(){
            const response = await this.sendReqest(window.location, "get")
            this.tasks = await response.json()
        },

        async createTask(){
            await this.getTasks()
            await this.sendReqest(
                window.location + "create", 
                "post", 
                JSON.stringify(this.task)
            )
            await this.getTasks()

            this.task.title = ""
            this.task.description = ""
        },
        
        async deleteTask(task){
            await this.sendReqest(
                window.location + "delete", 
                "post",
                JSON.stringify(task)
            )

            await this.getTasks()
        },

        async editTask(task){
            await this.sendReqest(
                window.location + "edit", 
                "post",
                JSON.stringify(task)
            )

            await this.getTasks()
        }
    },

    delimiters: ['{', '}']
}

createApp(TaskApp).mount('#app')