import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";


import {
  getTender,
  getTenderDocuments,
  getCriteria,
  getBidders,
} from "../services/tenderService";

function TenderDetails() {
  const { tenderId } = useParams();

  const navigate = useNavigate();

  const [tender, setTender] = useState(null);

  const [documents, setDocuments] = useState([]);

  const [criteria, setCriteria] = useState([]);

  const [bidders, setBidders] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  useEffect(() => {
    loadTender();
  }, []);

  async function loadTender() {
    try {
      const tenderData = await getTender(tenderId);

      setTender(tenderData);

      const docs = await getTenderDocuments(tenderId);

      setDocuments(docs);

      const criteriaList = await getCriteria(tenderId);

      setCriteria(criteriaList);

      const bidderList = await getBidders(tenderId);

      setBidders(bidderList);
    } catch (err) {
      console.error(err);

      setError("Unable to load Tender.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <h3>Loading...</h3>;
  }

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div className="container">
      <h2 className="mb-4">Tender Details</h2>

      <div className="card mb-4">
        <div className="card-header bg-primary text-white">
          Tender Information
        </div>

        <div className="card-body">
          <table className="table">
            <tbody>
              <tr>
                <th width="25%">Tender Number</th>

                <td>{tender.tender_number}</td>
              </tr>

              <tr>
                <th>Title</th>

                <td>{tender.title}</td>
              </tr>

              <tr>
                <th>Department</th>

                <td>{tender.department}</td>
              </tr>

              <tr>
                <th>Issue Date</th>

                <td>{tender.issue_date}</td>
              </tr>

              <tr>
                <th>Closing Date</th>

                <td>{tender.closing_date}</td>
              </tr>

              <tr>
                <th>Status</th>

                <td>
                  <span className="badge bg-success">{tender.status}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-header bg-secondary text-white d-flex justify-content-between align-items-center">
          <span>Tender Documents</span>

          <button
            className="btn btn-light btn-sm"
            onClick={() => navigate(`/tenders/${tenderId}/upload-document`)}
          >
            + Upload Document
          </button>
        </div>

        <div className="card-body">
          {documents.length === 0 ? (
            <div className="alert alert-warning mb-0">
              No documents uploaded for this tender.
            </div>
          ) : (
            <table className="table table-bordered table-hover">
              <thead className="table-light">
                <tr>
                  <th>File Name</th>

                  <th>Document Type</th>

                  <th>Status</th>

                  <th>Uploaded At</th>
                </tr>
              </thead>

              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.id}>
                    <td>{doc.original_filename}</td>

                    <td>{doc.document_type}</td>

                    <td>
                      <span className="badge bg-success">{doc.status}</span>
                    </td>

                    <td>{doc.uploaded_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-header bg-secondary text-white">
          Evaluation Criteria
        </div>

        <div className="card-body">
          {criteria.length === 0 ? (
            <div className="alert alert-warning mb-0">
              No criteria extracted.
            </div>
          ) : (
            <table className="table table-bordered table-hover">
              <thead className="table-light">
                <tr>
                  <th width="5%">#</th>

                  <th width="30%">Title</th>

                  <th>Description</th>

                  <th width="12%">Mandatory</th>
                </tr>
              </thead>

              <tbody>
                {criteria.map((c, index) => (
                  <tr key={c.id}>
                    <td>{index + 1}</td>

                    <td>{c.title}</td>

                    <td>{c.description}</td>

                    <td>
                      {c.mandatory ? (
                        <span className="badge bg-danger">Yes</span>
                      ) : (
                        <span className="badge bg-secondary">No</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-header bg-secondary text-white">
          Registered Bidders
        </div>

        <div className="card-body">
          {bidders.length === 0 ? (
            <div className="alert alert-warning mb-0">
              No bidders registered.
            </div>
          ) : (
            <table className="table table-bordered table-hover">
              <thead className="table-light">
                <tr>
                  <th width="5%">#</th>

                  <th>Bidder Name</th>

                  <th>Contact Person</th>

                  <th>Email</th>

                  <th>Phone</th>

                  <th width="10%">Action</th>
                </tr>
              </thead>

              <tbody>
                {bidders.map((bidder, index) => (
                  <tr key={bidder.id}>
                    <td>{index + 1}</td>

                    <td>{bidder.bidder_name}</td>

                    <td>{bidder.contact_person}</td>

                    <td>{bidder.email}</td>

                    <td>{bidder.phone}</td>

                    <td>
                      <button
                        className="btn btn-success btn-sm"
                        onClick={() => navigate("/evaluation/" + bidder.id)}
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default TenderDetails;
