import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  getTender,
  getTenderDocuments,
  getCriteria,
  getBidders,
  extractCriteria,
  deleteTenderDocument,
  deleteBidder,
  getTenderEvaluationReport,
  downloadTenderExcelReport,
  downloadTenderPDFReport,
} from "../services/tenderService";

function TenderDetails() {
  const { tenderId } = useParams();

  const navigate = useNavigate();

  const [tender, setTender] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [criteria, setCriteria] = useState([]);
  const [bidders, setBidders] = useState([]);

  const [loading, setLoading] = useState(true);
  const [extracting, setExtracting] = useState(false);
  const [evaluationReport, setEvaluationReport] = useState(null);
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

      try {
        const report = await getTenderEvaluationReport(tenderId);

        console.log("Tender Evaluation Report:", report);

        setEvaluationReport(report);
      } catch {
        setEvaluationReport(null);
      }
    } catch (err) {
      console.error(err);

      setError("Unable to load Tender.");
    } finally {
      setLoading(false);
    }
  }

  async function handleExtractCriteria() {
    try {
      setExtracting(true);

      await extractCriteria(tenderId);

      const criteriaList = await getCriteria(tenderId);

      setCriteria(criteriaList);

      alert("Criteria extracted successfully.");
    } catch (err) {
      console.error(err);

      alert("Criteria extraction failed.");
    } finally {
      setExtracting(false);
    }
  }

  async function handleDeleteDocument(documentId) {
    const confirmed = window.confirm(
      "Delete the Active NIT?\n\n" +
        "This will remove:\n\n" +
        "• PDF\n" +
        "• OCR Text\n" +
        "• Extracted Criteria\n\n" +
        "The Tender will remain.",
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteTenderDocument(documentId);

      alert("NIT deleted successfully.");

      await loadTender();
    } catch (err) {
      console.error(err);

      alert(err.response?.data?.detail || "Unable to delete NIT.");
    }
  }

  if (loading) {
    return <h3>Loading...</h3>;
  }

  console.log("First bidder:", evaluationReport?.bidders?.[0]);

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  return (
    <div className="container">
      <h2 className="mb-4">Tender Details</h2>

      {/* Tender Information */}

      <div className="card mb-4">
        <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
          <span>Tender Information</span>

          <button
        className="btn btn-secondary"
        onClick={() => navigate("/")}
    >
        🏠 Home
    </button>

          <button
            className="btn btn-light btn-sm"
            onClick={async () => {
              try {
                const blob = await downloadTenderPDFReport(tenderId);
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = `Tender_Evaluation_Report_${tenderId}.pdf`;
                link.click();
                window.URL.revokeObjectURL(url);
              } catch (err) {
                console.error(err);
                alert("Unable to download PDF report.");
              }
            }}
          >
            Download PDF Report
          </button>

          <button
            className="btn btn-light btn-sm"
            onClick={async () => {
              try {
                const blob = await downloadTenderExcelReport(tenderId);
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = "Tender_Evaluation_Report.xlsx";
                link.click();
                window.URL.revokeObjectURL(url);
              } catch (err) {
                console.error(err);
                alert("Unable to download Excel report.");
              }
            }}
          >
            Download Excel Report
          </button>
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

      {/* Tender Documents */}

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
            <div className="alert alert-warning">No documents uploaded.</div>
          ) : (
            documents.map((doc) => (
              <div key={doc.id} className="card mb-3 shadow-sm">
                <div className="card-body">
                  <div className="d-flex justify-content-between">
                    <div>
                      <h5 className="mb-3">📄 {doc.original_filename}</h5>

                      <table className="table table-sm table-borderless">
                        <tbody>
                          <tr>
                            <th width="140">Type</th>

                            <td>{doc.document_type}</td>
                          </tr>

                          <tr>
                            <th>Status</th>

                            <td>
                              <span className="badge bg-success">
                                {doc.status}
                              </span>
                            </td>
                          </tr>

                          <tr>
                            <th>Uploaded</th>

                            <td>
                              {new Date(doc.uploaded_at).toLocaleString()}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>

                    <div className="text-end">
                      <button className="btn btn-outline-primary btn-sm mb-2">
                        View
                      </button>

                      <br />

                      <button className="btn btn-outline-success btn-sm mb-2">
                        Download
                      </button>

                      {doc.document_type === "NIT" && (
                        <>
                          <br />

                          <button
                            className="btn btn-outline-danger btn-sm"
                            onClick={() => handleDeleteDocument(doc.id)}
                          >
                            Delete NIT
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Evaluation Criteria */}

      <div className="card mb-4">
        <div className="card-header bg-secondary text-white d-flex justify-content-between align-items-center">
          <span>Evaluation Criteria</span>

          <button
            className="btn btn-warning btn-sm"
            onClick={handleExtractCriteria}
            disabled={extracting}
          >
            {extracting ? "Extracting..." : "Extract Criteria"}
          </button>
        </div>

        <div className="card-body">
          {criteria.length === 0 ? (
            <div className="alert alert-warning">No criteria extracted.</div>
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

      {/* Tender Evaluation Summary */}

      <div className="card mb-4">
        <div className="card-header bg-success text-white">
          Tender Evaluation Summary
        </div>

        <div className="card-body">
          {!evaluationReport ? (
            <div className="alert alert-warning">
              No evaluation has been completed yet.
            </div>
          ) : (
            <>
              <div className="row mb-4">
                <div className="col-md-3">
                  <div className="card text-center">
                    <div className="card-body">
                      <h5>{evaluationReport.summary.total_bidders}</h5>
                      <small>Total Bidders</small>
                    </div>
                  </div>
                </div>

                <div className="col-md-3">
                  <div className="card text-center">
                    <div className="card-body">
                      <h5>{evaluationReport.summary.evaluated}</h5>
                      <small>Evaluated</small>
                    </div>
                  </div>
                </div>

                <div className="col-md-3">
                  <div className="card text-center">
                    <div className="card-body">
                      <h5>{evaluationReport.summary.pending}</h5>
                      <small>Pending</small>
                    </div>
                  </div>
                </div>

                <div className="col-md-3">
                  <div className="card text-center">
                    <div className="card-body">
                      <h5>{evaluationReport.summary.total_criteria}</h5>
                      <small>Criteria</small>
                    </div>
                  </div>
                </div>
              </div>

              <table className="table table-bordered table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Bidder</th>

                    <th>Complied</th>

                    <th>Partial</th>

                    <th>Not Complied</th>

                    <th>Not Found</th>

                    <th>Needs Review</th>

                    <th>Total Score</th>
                  </tr>
                </thead>

                <tbody>
                  {evaluationReport.bidders.map((b) => (
                    <tr key={b.bidder_id}>
                      <td>{b.name}</td>

                      <td className="text-success">{b.complied}</td>

                      <td>{b.partial}</td>
                      <td className="text-danger">{b.not_complied}</td>

                      <td>{b.not_found}</td>

                      <td>{b.needs_review}</td>

                      <td>
                        <strong>
                          {b.complied} /{" "}
                          {evaluationReport.summary.total_criteria}
                        </strong>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>
      </div>
      {/* Registered Bidders */}

      <div className="card mb-4">
        <div className="card-header bg-secondary text-white d-flex justify-content-between align-items-center">
          <span>Registered Bidders</span>

          <button
            className="btn btn-light btn-sm"
            onClick={() => navigate(`/tenders/${tenderId}/register-bidder`)}
          >
            + Register Bidder
          </button>
        </div>

        <div className="card-body">
          {bidders.length === 0 ? (
            <div className="alert alert-warning">No bidders registered.</div>
          ) : (
            <table className="table table-bordered table-hover">
              <thead className="table-light">
                <tr>
                  <th>#</th>

                  <th>Bidder Name</th>

                  <th>Contact Person</th>

                  <th>Email</th>

                  <th>Phone</th>

                  <th>Action</th>
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
                      <div className="d-flex gap-2">
                        <button
                          className="btn btn-success btn-sm"
                          onClick={() => navigate("/bidders/" + bidder.id)}
                        >
                          View
                        </button>

                        <button
                          className="btn btn-danger btn-sm"
                          onClick={async () => {
                            const confirmed = window.confirm(
                              `Delete bidder "${bidder.bidder_name}"?\n\n` +
                                "This will permanently delete:\n\n" +
                                "• Bidder Registration\n" +
                                "• Technical Bid Documents\n" +
                                "• Embeddings\n" +
                                "• Evaluation Results\n\n" +
                                "This action cannot be undone.",
                            );

                            if (!confirmed) return;

                            try {
                              await deleteBidder(bidder.id);

                              alert("Bidder deleted successfully.");

                              await loadTender();
                            } catch (err) {
                              console.error(err);

                              alert(
                                err.response?.data?.detail ||
                                  "Unable to delete bidder.",
                              );
                            }
                          }}
                        >
                          Delete
                        </button>
                      </div>
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
