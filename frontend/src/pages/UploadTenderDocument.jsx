import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { uploadTenderDocument } from "../services/tenderService";

function UploadTenderDocument() {

    const { tenderId } = useParams();

    const navigate = useNavigate();

    const [documentType, setDocumentType] = useState("NIT");

    const [file, setFile] = useState(null);

    // async function upload() {

    //     if (!file) {

    //         alert("Please select a file.");

    //         return;

    //     }

    //     const formData = new FormData();

    //     formData.append("document_type", documentType);

    //     formData.append("file", file);

    //     await uploadTenderDocument(
    //         tenderId,
    //         formData
    //     );

    //     alert("Document uploaded successfully.");

    //     navigate("/tenders/" + tenderId);

    // }

    async function upload() {

    if (!file) {

        alert("Please select a file.");

        return;

    }

    const formData = new FormData();

    formData.append("document_type", documentType);

    formData.append("file", file);

    try {

        await uploadTenderDocument(
            tenderId,
            formData
        );

        alert("Document uploaded successfully.");

        navigate("/tenders/" + tenderId);

    }
    catch (err) {

        if (err.response?.data?.detail) {

            alert(err.response.data.detail);

        }
        else {

            alert("Unable to upload document.");

            console.error(err);

        }

    }

}

    return (

        <div className="container mt-4">


            <div className="card">

                <div className="card-header bg-primary text-white">

                    Upload Tender Document

                </div>

                <div className="card-body">

                    <div className="mb-3">

                        <label className="form-label">

                            Document Type

                        </label>

                        <select
                            className="form-select"
                            value={documentType}
                            onChange={(e) => setDocumentType(e.target.value)}
                        >

                            <option value="NIT">NIT</option>

                            <option value="CORRIGENDUM">Corrigendum</option>

                            

                             </select>

                    </div>

                    <div className="mb-3">

                        <label className="form-label">

                            PDF Document

                        </label>

                        <input
                            type="file"
                            className="form-control"
                            accept=".pdf"
                            onChange={(e) =>
                                setFile(e.target.files[0])
                            }
                        />

                    </div>

                    <button
                        className="btn btn-success"
                        onClick={upload}
                    >
                        Upload
                    </button>

                </div>

            </div>

        </div>

    );

}

export default UploadTenderDocument;