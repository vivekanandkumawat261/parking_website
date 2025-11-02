import { createWebHistory, createRouter } from "vue-router"
import Content from './components/Content.vue'
import LoginPage from "./components/LoginPage.vue"
import RegisterPage from "./components/RegisterPage.vue"
import Dashboard from "./components/Dashboard.vue"
import RequestSpot from "./components/RequestSpot.vue"
import AddLots from "./components/AddLots.vue"
import EditParkingLot from "./components/EditParkingLot.vue"
import AdminUsers from "./components/AdminUsers.vue"
import SearchBar from "./components/SearchBar.vue"
import AdminSummary from "./components/AdminSummary.vue"
import ViewSpot from "./components/ViewSpot.vue"


const routes = [
    {path: "/", component: Content},
    {path: "/login", component: LoginPage},
    {path:"/register", component: RegisterPage},
    {path: "/dashboard",component: Dashboard},
    {path: "/user/reserve",component: RequestSpot},
    {path: "/admin/parkinglots",component: AddLots},
    {path: "/admin/edit-lot/:id", component: EditParkingLot},
    {path: "/admin/users", component:AdminUsers},
    {path: "/admin/search", component:SearchBar},
    { path: '/admin/summary', component: AdminSummary },
    {path: '/admin/view-spot/:id', component: ViewSpot},
    // {psth: "/user", component: [
    //     {path: '',component: User},
    //     {path: "request/:cardname", component: RequestCard},
    //     {path: "view/:cardname", component: ViewCard}
    //     ],
    // }
]

export const router = createRouter({
    history: createWebHistory(),
    routes // -> routes: routes
})