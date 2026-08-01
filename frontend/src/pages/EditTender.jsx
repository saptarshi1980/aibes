import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import TenderForm from "../components/TenderForm";

import {
    getTender,
    updateTender,
} from "../services/tenderService";

function EditTender() {

    const { tenderId } = useParams();

    const navigate = useNavigate();

    const [tender, setTender] = useState(null);

    useEffect(() => {

        loadTender();

    }, []);

    async function loadTender() {

        const data = await getTender(tenderId);

        setTender(data);

    }

    async function saveTender(formData) {

        await updateTender(
            tenderId,
            formData
        );

        alert("Tender updated successfully.");

        navigate("/tenders");

    }

    if (!tender) {

        return (
            <div className="container mt-4">
                Loading...
            </div>
        );

    }

    return (

        <div className="container mt-4">

            <div className="card">

                <div className="card-header bg-warning">

                    Edit Tender

                    <button
        className="btn btn-secondary"
        onClick={() => navigate("/")}
    >
        🏠 Home
    </button>

                </div>

                <div className="card-body">

                    <TenderForm
                        initialData={tender}
                        onSubmit={saveTender}
                        buttonText="Update Tender"
                    />

                </div>

            </div>

        </div>

    );

}

export default EditTender;