import { useNavigate } from "react-router-dom";

import TenderForm from "../components/TenderForm";

import { createTender } from "../services/tenderService";

function CreateTender() {

    const navigate = useNavigate();

    async function saveTender(data) {

        await createTender(data);

        alert("Tender created successfully.");

        navigate("/tenders");
    }

    return (

        <div className="container mt-4">

            <div className="card">

                <div className="card-header bg-primary text-white">
                    Create Tender
                </div>

                <div className="card-body">

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