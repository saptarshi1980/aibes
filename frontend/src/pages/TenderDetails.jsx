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
  viewTenderDocument,
} from "../services/tenderService";

// Maps a status string to a Bootstrap badge color so the badge always
// reflects what actually happened, instead of always rendering green.
function statusBadgeClass(status) {
  const normalized = (status || "").toLowerCase();

  if (
    ["complete", "completed", "closed", "active", "processed"].includes(
      normalized,
    )
  ) {
    return "bg-success";
  }
  if (["pending", "processing", "in progress", "open"].includes(normalized)) {
    return "bg-warning text-dark";
  }
  if (["failed", "error", "rejected", "cancelled"].includes(normalized)) {
    return "bg-danger";
  }
  return "bg-secondary";
}

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

  // Per-action loading flags so a single button shows its own busy state
  // instead of the whole page locking up.
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [downloadingExcel, setDownloadingExcel] = useState(false);
  const [deletingDocId, setDeletingDocId] = useState(null);
  const [deletingBidderId, setDeletingBidderId] = useState(null);

  useEffect(() => {
    loadTender();
    // eslint-disable-next-line react-hooks/exhaustive-deps
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
        setEvaluationReport(report);
      } catch {
        setEvaluationReport(null);
      }
    } catch (err) {
      console.error(err);
      setError("Unable to load tender.");
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
    } catch (err) {
      console.error(err);
      alert("Criteria extraction failed.");
    } finally {
      setExtracting(false);
    }
  }

  async function handleDeleteDocument(documentId) {
    const confirmed = window.confirm(
      "Delete the active NIT?\n\n" +
        "This will remove:\n\n" +
        "• PDF\n" +
        "• OCR text\n" +
        "• Extracted criteria\n\n" +
        "The tender will remain.",
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeletingDocId(documentId);
      await deleteTenderDocument(documentId);
      await loadTender();
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Unable to delete NIT.");
    } finally {
      setDeletingDocId(null);
    }
  }

  async function handleDeleteBidder(bidder) {
    const confirmed = window.confirm(
      `Delete bidder "${bidder.bidder_name}"?\n\n` +
        "This will permanently delete:\n\n" +
        "• Bidder registration\n" +
        "• Technical bid documents\n" +
        "• Embeddings\n" +
        "• Evaluation results\n\n" +
        "This action cannot be undone.",
    );

    if (!confirmed) return;

    try {
      setDeletingBidderId(bidder.id);
      await deleteBidder(bidder.id);
      await loadTender();
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.detail || "Unable to delete bidder.");
    } finally {
      setDeletingBidderId(null);
    }
  }

  async function handleDownloadPdf() {
    try {
      setDownloadingPdf(true);
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
    } finally {
      setDownloadingPdf(false);
    }
  }

  async function handleDownloadExcel() {
    try {
      setDownloadingExcel(true);
      const blob = await downloadTenderExcelReport(tenderId);
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `Tender_Evaluation_Report_${tenderId}.xlsx`;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Unable to download Excel report.");
    } finally {
      setDownloadingExcel(false);
    }
  }

  if (loading) {
    return (
      <div className="d-flex flex-column align-items-center justify-content-center py-5 text-secondary">
        <div className="spinner-border mb-3" role="status">
          <span className="visually-hidden">Loading…</span>
        </div>
        <div>Loading tender…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container py-4">
        <div className="alert alert-danger d-flex justify-content-between align-items-center">
          <span>{error}</span>
          <button
            className="btn btn-outline-danger btn-sm"
            onClick={() => navigate("/")}
          >
            Back to home
  
          </button>
        </div>
      </div>
    );
  }



  return (
    <div className="container py-4">
      {/* Page header */}
      <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-4">
        <div>
          <button
            className="btn btn-link ps-0 text-decoration-none mb-2"
            onClick={() => navigate("/")}
          >
            ← Back to tenders
          </button>
          <h2 className="mb-1">{tender.title}</h2>
          <div className="text-secondary">
            Tender #{tender.tender_number} · {tender.department}
          </div>
        </div>

        <div className="d-flex justify-content-end gap-2 w-100 ms-auto">
          <button
            className="btn btn-outline-secondary"
            onClick={handleDownloadPdf}
            disabled={downloadingPdf}
          >
            {downloadingPdf ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" />
                Preparing…
              </>
            ) : (
              "⬇ Evaluation Report (PDF)"
            )}
          </button>

          <button
            className="btn btn-outline-secondary"
            onClick={handleDownloadExcel}
            disabled={downloadingExcel}
          >
            {downloadingExcel ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" />
                Preparing…
              </>
            ) : (
              "⬇ Evaluation Report (Excel)"
            )}
          </button>
        </div>
      </div>

      {/* Tender Information */}
      <div className="card mb-4 shadow-sm">
        <div className="card-header bg-primary text-white">
          Tender Information
        </div>

        <div className="card-body">
          <div className="table-responsive">
            <table className="table table-sm mb-0">
              <tbody>
                <tr>
                  <th className="text-secondary" style={{ width: "25%" }}>
                    Tender Number
                  </th>
                  <td>{tender.tender_number}</td>
                </tr>
                <tr>
                  <th className="text-secondary">Title</th>
                  <td>{tender.title}</td>
                </tr>
                <tr>
                  <th className="text-secondary">Department</th>
                  <td>{tender.department}</td>
                </tr>
                <tr>
                  <th className="text-secondary">Issue Date</th>
                  <td>{tender.issue_date}</td>
                </tr>
                <tr>
                  <th className="text-secondary">Closing Date</th>
                  <td>{tender.closing_date}</td>
                </tr>
                <tr>
                  <th className="text-secondary">Status</th>
                  <td>
                    <span
                      className={`badge ${statusBadgeClass(tender.status)}`}
                    >
                      {tender.status}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Tender Documents */}
      <div className="card mb-4 shadow-sm">
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
            <div className="text-center text-secondary py-4">
              <div className="fs-2 mb-2">📄</div>
              <div>No documents uploaded yet.</div>
            </div>
          ) : (
            <div className="d-flex flex-column gap-3">
              {documents.map((doc) => (
                <div key={doc.id} className="card">
                  <div className="card-body">
                    <div className="d-flex flex-wrap justify-content-between gap-3">
                      <div>
                        <h6 className="mb-2">📄 {doc.original_filename}</h6>

                        <div className="d-flex flex-wrap gap-4 small text-secondary">
                          <div>
                            <span className="fw-semibold text-body">
                              Type:{" "}
                            </span>
                            {doc.document_type}
                          </div>
                          <div>
                            <span className="fw-semibold text-body">
                              Status:{" "}
                            </span>
                            <span
                              className={`badge ${statusBadgeClass(doc.status)}`}
                            >
                              {doc.status}
                            </span>
                          </div>
                          <div>
                            <span className="fw-semibold text-body">
                              Uploaded:{" "}
                            </span>
                            {new Date(doc.uploaded_at).toLocaleString()}
                          </div>
                        </div>
                      </div>

                      <div className="d-flex align-items-start gap-2">
                        <button
                          className="btn btn-outline-primary btn-sm mb-2"
                          onClick={async () => {
                            try {
                              const blob = await viewTenderDocument(doc.id);

                              const url = window.URL.createObjectURL(blob);

                              window.open(url, "_blank");
                            } catch (err) {
                              console.error(err);

                              alert("Unable to open PDF.");
                            }
                          }}
                        >
                          View
                        </button>
                        

                        {doc.document_type === "NIT" && (
                          <button
                            className="btn btn-outline-danger btn-sm"
                            onClick={() => handleDeleteDocument(doc.id)}
                            disabled={deletingDocId === doc.id}
                          >
                            {deletingDocId === doc.id ? (
                              <span className="spinner-border spinner-border-sm" />
                            ) : (
                              "Delete NIT"
                            )}
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Evaluation Criteria */}
      <div className="card mb-4 shadow-sm">
        <div className="card-header bg-secondary text-white d-flex justify-content-between align-items-center">
          <span>Evaluation Criteria</span>

          <button
            className="btn btn-warning btn-sm"
            onClick={handleExtractCriteria}
            disabled={extracting}
          >
            {extracting ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" />
                Extracting…
              </>
            ) : (
              "Extract Criteria"
            )}
          </button>
        </div>

        <div className="card-body">
          {criteria.length === 0 ? (
            <div className="text-center text-secondary py-4">
              <div className="fs-2 mb-2">📋</div>
              <div>
                No criteria extracted yet. Click "Extract Criteria" to get
                started.
              </div>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-bordered table-hover align-middle mb-0">
                <thead className="table-light">
                  <tr>
                    <th style={{ width: "5%" }}>#</th>
                    <th style={{ width: "30%" }}>Title</th>
                    <th>Description</th>
                    <th style={{ width: "12%" }}>Mandatory</th>
                  </tr>
                </thead>

                <tbody>
                  {criteria.map((c, index) => (
                    <tr key={c.id}>
                      <td>{index + 1}</td>
                      <td className="fw-semibold">{c.title}</td>
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
            </div>
          )}
        </div>
      </div>

      {/* Tender Evaluation Summary */}
      <div className="card mb-4 shadow-sm">
        <div className="card-header bg-success text-white">
          Tender Evaluation Summary
        </div>

        <div className="card-body">
          {!evaluationReport ? (
            <div className="text-center text-secondary py-4">
              <div className="fs-2 mb-2">📊</div>
              <div>No evaluation has been completed yet.</div>
            </div>
          ) : (
            <>
              <div className="row g-3 mb-4">
                <div className="col-6 col-md-3">
                  <div className="card text-center h-100">
                    <div className="card-body">
                      <h4 className="mb-1">
                        {evaluationReport.summary.total_bidders}
                      </h4>
                      <small className="text-secondary">Total Bidders</small>
                    </div>
                  </div>
                </div>

                <div className="col-6 col-md-3">
                  <div className="card text-center h-100">
                    <div className="card-body">
                      <h4 className="mb-1 text-success">
                        {evaluationReport.summary.evaluated}
                      </h4>
                      <small className="text-secondary">Evaluated</small>
                    </div>
                  </div>
                </div>

                <div className="col-6 col-md-3">
                  <div className="card text-center h-100">
                    <div className="card-body">
                      <h4 className="mb-1 text-warning">
                        {evaluationReport.summary.pending}
                      </h4>
                      <small className="text-secondary">Pending</small>
                    </div>
                  </div>
                </div>

                <div className="col-6 col-md-3">
                  <div className="card text-center h-100">
                    <div className="card-body">
                      <h4 className="mb-1">
                        {evaluationReport.summary.total_criteria}
                      </h4>
                      <small className="text-secondary">Criteria</small>
                    </div>
                  </div>
                </div>
              </div>

              <div className="table-responsive">
                <table className="table table-bordered table-hover align-middle mb-0">
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
                      <tr key={b.id}>
                        <td className="fw-semibold">{b.name}</td>
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
              </div>
            </>
          )}
        </div>
      </div>

      {/* Registered Bidders */}
      <div className="card mb-4 shadow-sm">
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
            <div className="text-center text-secondary py-4">
              <div className="fs-2 mb-2">🧑‍💼</div>
              <div>No bidders registered yet.</div>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-bordered table-hover align-middle mb-0">
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
                      <td className="fw-semibold">{bidder.bidder_name}</td>
                      <td>{bidder.contact_person}</td>
                      <td>{bidder.email}</td>
                      <td>{bidder.phone}</td>
                      <td>
                        <div className="d-flex gap-2">
                          <button
                            className="btn btn-outline-success btn-sm"
                            onClick={() => navigate("/bidders/" + bidder.id)}
                          >
                            View
                          </button>

                          <button
                            className="btn btn-outline-danger btn-sm"
                            onClick={() => handleDeleteBidder(bidder)}
                            disabled={deletingBidderId === bidder.id}
                          >
                            {deletingBidderId === bidder.id ? (
                              <span className="spinner-border spinner-border-sm" />
                            ) : (
                              "Delete"
                            )}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TenderDetails;
