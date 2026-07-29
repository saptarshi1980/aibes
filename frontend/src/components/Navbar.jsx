import { Link } from "react-router-dom";

function Navbar() {

    return (

        <nav className="navbar navbar-expand-lg navbar-light bg-light">

            <div className="container">

                <Link
                    className="btn btn-outline-primary me-2"
                    to="/"
                >
                    Dashboard
                </Link>

                <Link
                    className="btn btn-outline-primary me-2"
                    to="/tenders"
                >
                    Tenders
                </Link>

                <Link
                    className="btn btn-outline-primary me-2"
                    to="/bidders"
                >
                    Bidders
                </Link>

                <Link
                    className="btn btn-outline-primary"
                    to="/evaluation"
                >
                    Evaluation
                </Link>

            </div>

        </nav>

    );

}

export default Navbar;