import { createWebHistory, createRouter } from "vue-router"; // important to create the router 

// import components here to  register to main.js
import FirstPage from "./components/FirstPage.vue";
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";
import AdminDash from "./components/AdminDash.vue";
import AddLot from "./components/AddLot.vue";
import EditLot from "./components/EditLot.vue";
import AdminUsers from "./components/AdminUsers.vue";
import AdminSummary from "./components/AdminSummary.vue";
import OccupiedStatus from "./components/OccupiedStatus.vue";
import ViewParkingInfo from "./components/ViewParkingInfo.vue";
import UserDash from "./components/UserDash.vue";
import UserBooking from "./components/UserBooking.vue";
import UserRelease from "./components/UserRelease.vue";
import EditProfile from "./components/EditProfile.vue";
import UserSummary from "./components/UserSummary.vue";


const routes = [
    // general routes for both admin and user
    { path: "/", component: FirstPage },
    { path: "/login", component: Login },
    { path: "/register", component: Register },

    // admin routes are there 
    { path: "/admin", component: AdminDash },
    { path: "/admin/add_lot", component: AddLot },
    { path: "/admin/edit_lot/:id", component: EditLot },
    { path: "/admin/users", component: AdminUsers },
    { path: "/admin/summary", component: AdminSummary },
    { path: "/admin/spot_info/:lot_id/:spot_number", component: OccupiedStatus },
    { path: "/admin/view_parking/:lot_id/:spot_number", component: ViewParkingInfo },

    // user routes are these using dynamic routing as well
    { path: "/user/:id", component: UserDash },
    { path: "/user/book/:lot_id/:user_id", component: UserBooking },
    { path: "/user/release/:id", component: UserRelease },
    { path: "/user/edit/:id", component: EditProfile },
    { path: "/user/summary/:id", component: UserSummary }
];


export const router = createRouter({
    history: createWebHistory(),  // this stores info of the different routes and is actually where routes can be rerouted
    routes
});