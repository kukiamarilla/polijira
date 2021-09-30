import store from "@/store";

export default function auth({to, next, router}) {
    if(store.state.proyecto.me.proyecto.id != to.params["id"])
        store.dispatch("proyecto/getMe", to.params["id"]).then(() =>{
            next()
        }
        ).catch(() => {
            router.push("/")
        })
    else
        next()
    
}
