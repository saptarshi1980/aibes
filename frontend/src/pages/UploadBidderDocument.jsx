import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { uploadBidderDocument } from "../services/tenderService";

function UploadBidderDocument() {

    const { bidderId } = useParams();

    const navigate = useNavigate();

    const [documentType, setDocumentType] = useState("TECHNICAL_BID");

    const [file, setFile] = useState(null);

    const [uploading, setUploading] = useState(false);

    async function upload() {

        if (!file) {

            alert("Please select a PDF file.");

            return;

        }

        const formData = new FormData();

        formData.append(
            "document_type",
            documentType
        );

        formData.append(
            "file",
            file
        );

        try {

            setUploading(true);

            await uploadBidderDocument(
                bidderId,
                formData
            );

            alert("Technical Bid uploaded successfully.");

            navigate("/bidders/" + bidderId);

        }

        catch (err) {

            console.error(err);

            alert("Upload failed.");

        }

        finally {

            setUploading(false);

        }

    }

    return (

        <div className="container mt-4">

            <div className="card">

                <div className="card-header bg-primary text-white">

                    Upload Technical Bid

                    <button
        className="btn btn-secondary"
        onClick={() => navigate("/")}
    >
        🏠 Home
    </button>

                </div>

                <div className="card-body">

                    <div className="mb-3">

                        <label className="form-label">

                            Document Type

                        </label>

                        <select

                            className="form-select"

                            value={documentType}

                            onChange={(e)=>
                                setDocumentType(
                                    e.target.value
                                )
                            }

                        >

                            <option value="TECHNICAL_BID">

                                Technical Bid

                            </option>

                        </select>

                    </div>

                    <div className="mb-3">

                        <label className="form-label">

                            PDF File

                        </label>

                        <input

                            type="file"

                            className="form-control"

                            accept=".pdf"

                            onChange={(e)=>
                                setFile(
                                    e.target.files[0]
                                )
                            }

                        />

                    </div>

                    <button

                        className="btn btn-success"

                        onClick={upload}

                        disabled={uploading}

                    >

                        {

                            uploading

                            ?

                            "Uploading..."

                            :

                            "Upload"

                        }

                    </button>

                </div>

            </div>

        </div>

    );

}

export default UploadBidderDocument;