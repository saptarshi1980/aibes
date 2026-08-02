import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  getBidder,
  getBidderDocuments,
  evaluateBidder,
  generateBidderIndex,
  getEmbeddingStatus,
  getEvaluationStatus,
  generateClarificationLetter,
} from "../services/tenderService";

function BidderWorkspace() {
  const { bidderId } = useParams();

  const navigate = useNavigate();

  const [bidder, setBidder] = useState(null);

  const [documents, setDocuments] = useState([]);

  const [loading, setLoading] = useState(true);

  const [evaluating, setEvaluating] = useState(false);

  const [indexing, setIndexing] = useState(false);
  const [alreadyEvaluated, setAlreadyEvaluated] = useState(false);

  const [embeddingsGenerated, setEmbeddingsGenerated] = useState(false);

  useEffect(() => {
    load();
  }, []);

  // async function load() {

  //    console.log("LOAD CALLED");

  //   setLoading(true);

  //   const bidderData = await getBidder(bidderId);

  //   setBidder(bidderData);

  //   const docs = await getBidderDocuments(bidderId);

  //   setDocuments(docs);

  //   //
  //   // Embedding Status
  //   //
  //   try {
  //     const status = await getEmbeddingStatus(bidderId);
  //     console.log("Embedding API Response:", status);

  //     console.log("Embedding Status API:", status);
  //     console.log("embeddingsGenerated should become:", status.generated);

  //     setEmbeddingsGenerated(status.generated);

  //     console.log("Embedding State:", status.generated);
  //     setEmbeddingsGenerated(status.generated);
  //   } catch {
  //     setEmbeddingsGenerated(false);
  //   }

  //   //
  //   // Evaluation Status
  //   //
  //   try {
  //     const status = await getEvaluationStatus(bidderId);

  //     setAlreadyEvaluated(status.evaluated);
  //   } catch {
  //     setAlreadyEvaluated(false);
  //   }

  //   setLoading(false);
  // }

  async function load() {
    console.log("LOAD CALLED");

    setLoading(true);

    try {
      console.log("Calling getBidder...");

      const bidderData = await getBidder(bidderId);

      console.log("getBidder DONE");

      setBidder(bidderData);

      console.log("Calling getBidderDocuments...");

      const docs = await getBidderDocuments(bidderId);

      console.log("getBidderDocuments DONE");

      setDocuments(docs);

      console.log("Calling getEmbeddingStatus...");

      const status = await getEmbeddingStatus(bidderId);

      console.log("getEmbeddingStatus DONE", status);

      setEmbeddingsGenerated(status.generated);

      console.log("Calling getEvaluationStatus...");

      const evalStatus = await getEvaluationStatus(bidderId);

      console.log("getEvaluationStatus DONE", evalStatus);

      setAlreadyEvaluated(evalStatus.evaluated);
    } catch (err) {
      console.error("LOAD ERROR", err);
    }

    setLoading(false);
  }

  if (loading) return <h3>Loading...</h3>;

  const technicalBidUploaded = documents.length > 0;

  return (
    <div className="container mt-4">
      <h2>Bidder Workspace</h2>
      <button className="btn btn-secondary" onClick={() => navigate("/")}>
        🏠 Home
      </button>
      <div className="card mb-4">
        <div className="card-header bg-primary text-white">
          Bidder Information
        </div>

        <div className="card-body">
          <table className="table">
            <tbody>
              <tr>
                <th width="200">Bidder Name</th>

                <td>{bidder.bidder_name}</td>
              </tr>

              <tr>
                <th>Contact Person</th>

                <td>{bidder.contact_person}</td>
              </tr>

              <tr>
                <th>Email</th>

                <td>{bidder.email}</td>
              </tr>

              <tr>
                <th>Phone</th>

                <td>{bidder.phone}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-header bg-secondary text-white d-flex justify-content-between">
          <span>Technical Bid Documents</span>

          <button
            className="btn btn-light btn-sm"
            disabled={indexing}
            onClick={() => navigate(`/bidders/${bidderId}/upload`)}
          >
            + Upload Technical Bid
          </button>
        </div>

        <div className="card-body">
          {documents.length === 0 ? (
            <div className="alert alert-warning">
              No technical bid uploaded.
            </div>
          ) : (
            <table className="table table-bordered">
              <thead>
                <tr>
                  <th>File</th>

                  <th>Status</th>

                  <th>Uploaded</th>
                </tr>
              </thead>

              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.id}>
                    <td>{doc.original_filename}</td>

                    <td>{doc.status}</td>

                    <td>{new Date(doc.uploaded_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-header">Workflow Status</div>

        <div className="card-body">
          <p>
            <strong>Technical Bid</strong>{" "}
            {technicalBidUploaded ? (
              <span className="badge bg-success ms-2">Uploaded</span>
            ) : (
              <span className="badge bg-danger ms-2">Not Uploaded</span>
            )}
          </p>

          <p>
            <strong>Embeddings</strong>{" "}
            {embeddingsGenerated ? (
              <span className="badge bg-success ms-2">Generated</span>
            ) : (
              <span className="badge bg-warning text-dark ms-2">Pending</span>
            )}
          </p>
        </div>
      </div>

      {indexing && (
        <div className="alert alert-info">
          <strong>Generating embeddings...</strong>
          <br />
          This may take around one minute.
        </div>
      )}

      <div className="d-flex gap-2">
        <button
          className="btn btn-primary"
          disabled={indexing || !technicalBidUploaded}
          onClick={async () => {
            try {
              setIndexing(true);

              await generateBidderIndex(bidderId);

              await load();

              alert("Embeddings generated successfully.");
            } catch (err) {
              console.error(err);

              alert("Embedding generation failed.");
            } finally {
              setIndexing(false);
            }
          }}
        >
          {indexing ? "Generating..." : "Generate Embeddings"}
        </button>

        <button
          className="btn btn-success"
          disabled={evaluating || !embeddingsGenerated || alreadyEvaluated}
          onClick={async () => {
            try {
              setEvaluating(true);

              await evaluateBidder(bidderId);

              navigate("/evaluation/" + bidderId);
            } catch (err) {
              console.error(err);

              alert("Evaluation failed.");
            } finally {
              setEvaluating(false);
            }
          }}
        >
          {evaluating
            ? "Evaluating..."
            : alreadyEvaluated
              ? "Already Evaluated"
              : "Evaluate Bidder"}
        </button>

        <button
          className="btn btn-warning"
          onClick={async () => {
            const submissionDate = prompt("Submission Date (e.g. 15-Aug-2026)");

            if (!submissionDate) return;

            try {
              await generateClarificationLetter(bidderId, submissionDate);

              alert("Clarification letter generated successfully.");
            } catch (err) {
              console.error(err);

              alert("Unable to generate clarification letter.");
            }
          }}
        >
          Generate Clarification
        </button>
      </div>
    </div>
  );
}

export default BidderWorkspace;
