import Header from "./Header";
import Navbar from "./Navbar";
import { Outlet } from "react-router-dom";

function Layout() {

    return (

        <>

            <Header />

            <Navbar />

            <div className="container mt-3">

                <Outlet />

            </div>

        </>

    );

}

export default Layout;