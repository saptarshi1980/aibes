import { useNavigate } from "react-router-dom";

import TenderForm from "../components/TenderForm";

import { createTender } from "../services/tenderService";

function CreateTender() {

    const navigate = useNavigate();

    // async function saveTender(data) {

    //     await createTender(data);

    //     alert("Tender created successfully.");

    //     navigate("/tenders");
    // }

    async function saveTender(data) {

    try {

        await createTender(data);

        alert("Tender created successfully.");

        navigate("/tenders");

    }
    catch (err) {

        if (err.response?.data?.detail) {

            alert(err.response.data.detail);

        }
        else {

            alert("Unable to create Tender.");

            console.error(err);

        }

    }

}

    return (

        <div className="container mt-4">

            <div className="card">

                <div className="card-header bg-primary text-white">
                    Create Tender
                </div>

                <div className="card-body">
                    <button
        className="btn btn-secondary"
        onClick={() => navigate("/")}
    >
        🏠 Home
    </button>

                    <TenderForm
                        onSubmit={saveTender}
                        buttonText="Create Tender"
                    />

                </div>

            </div>

        </div>

    );

}

export default CreateTender;