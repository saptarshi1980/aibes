import { Outlet, Link } from "react-router-dom";

function Layout() {
  return (
    <>
      <nav className="navbar navbar-dark bg-primary shadow-sm">
        <div className="container-fluid">

          <div>
            <h4 className="text-white mb-0">
              AI Assisted Bid Evaluation System
            </h4>

            <small className="text-light">
              The Durgapur Projects Limited
            </small>
          </div>

          <Link
            to="/"
            className="btn btn-light"
          >
            🏠 Home
          </Link>

        </div>
      </nav>

      <div className="container mt-4">
        <Outlet />
      </div>
    </>
  );
}

export default Layout;