import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  getBidder,
  getBidderDocuments,
  evaluateBidder,
} from "../services/tenderService";

function BidderWorkspace() {
  const { bidderId } = useParams();

  const navigate = useNavigate();

  const [bidder, setBidder] = useState(null);

  const [documents, setDocuments] = useState([]);

  const [loading, setLoading] = useState(true);

  const [evaluating, setEvaluating] = useState(false);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    const bidderData = await getBidder(bidderId);

    setBidder(bidderData);

    const docs = await getBidderDocuments(bidderId);

    setDocuments(docs);

    setLoading(false);
  }

  if (loading) return <h3>Loading...</h3>;

  return (
    <div className="container mt-4">
      <h2>Bidder Workspace</h2>

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

      <button
        className="btn btn-success"
        disabled={evaluating}
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
        {evaluating ? "Evaluating..." : "Evaluate Bidder"}
      </button>
    </div>
  );
}

export default BidderWorkspace;
