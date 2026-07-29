import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getBidder,
  getEvaluationResults,
} from "../services/tenderService";

function EvaluationDetails() {
  const { bidderId } = useParams();

  const [bidder, setBidder] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const bidderData = await getBidder(bidderId);
      setBidder(bidderData);

      const evaluationResults = await getEvaluationResults(bidderId);
      setResults(evaluationResults);
    } catch (err) {
      console.error(err);
      setError("Unable to load evaluation details.");
    } finally {
      setLoading(false);
    }
  }

  // ===========================
  // Evaluation Summary
  // ===========================

  const totalCriteria = results.length;

  const complied = results.filter(
    (r) => r.status === "COMPLIED"
  ).length;

  const partial = results.filter(
    (r) => r.status === "PARTIALLY_COMPLIED"
  ).length;

  const manual = results.filter(
    (r) => r.status === "NEEDS_MANUAL_REVIEW"
  ).length;

  const notComplied = results.filter(
    (r) => r.status === "NOT_COMPLIED"
  ).length;

  const notFound = results.filter(
    (r) => r.status === "NOT_FOUND"
  ).length;

  if (loading) {
    return (
      <div className="container mt-4">
        <h3>Loading...</h3>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="container">

      <h2 className="mb-4">
        Technical Evaluation
      </h2>

      {/* ============================= */}
      {/* Bidder Information            */}
      {/* ============================= */}

      <div className="card mb-4">

        <div className="card-header bg-primary text-white">
          Bidder Information
        </div>

        <div className="card-body">

          <table className="table">

            <tbody>

              <tr>
                <th width="25%">Bidder Name</th>
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

      {/* ============================= */}
      {/* Evaluation Summary            */}
      {/* ============================= */}

      <div className="card mb-4">

        <div className="card-header bg-dark text-white">
          Evaluation Summary
        </div>

        <div className="card-body">

          <div className="row text-center">

            <div className="col-md-2">
              <h3>{totalCriteria}</h3>
              <small>Total Criteria</small>
            </div>

            <div className="col-md-2">
              <h3 className="text-success">
                {complied}
              </h3>
              <small>Complied</small>
            </div>

            <div className="col-md-2">
              <h3 className="text-warning">
                {partial}
              </h3>
              <small>Partial</small>
            </div>

            <div className="col-md-2">
              <h3 className="text-info">
                {manual}
              </h3>
              <small>Manual Review</small>
            </div>

            <div className="col-md-2">
              <h3 className="text-danger">
                {notComplied}
              </h3>
              <small>Not Complied</small>
            </div>

            <div className="col-md-2">
              <h3 className="text-secondary">
                {notFound}
              </h3>
              <small>Not Found</small>
            </div>

          </div>

          <hr />

          <h5>

            Recommendation :

            {" "}

            {notComplied === 0 ? (

              <span className="badge bg-success fs-6">
                TECHNICALLY QUALIFIED
              </span>

            ) : (

              <span className="badge bg-danger fs-6">
                NOT QUALIFIED
              </span>

            )}

          </h5>

        </div>

      </div>

      {/* ============================= */}
      {/* AI Evaluation Results         */}
      {/* ============================= */}

      <div className="card">

        <div className="card-header bg-success text-white">
          AI Evaluation Results
        </div>

        <div className="card-body">

          {results.length === 0 ? (

            <div className="alert alert-warning">
              No evaluation results available.
            </div>

          ) : (

            <table className="table table-bordered table-hover">

              <thead className="table-light">

                <tr>

                  <th width="30%">Criterion</th>

                  <th width="15%">Status</th>

                  <th width="10%">Confidence</th>

                  <th>Remarks</th>

                </tr>

              </thead>

              <tbody>

                {results.map((result) => (

                  <tr key={result.id}>

                    <td>

                      <strong>
                        {result.criterion_title}
                      </strong>

                    </td>

                    <td>

                      <span
                        className={
                          result.status === "COMPLIED"
                            ? "badge bg-success"
                            : result.status ===
                              "PARTIALLY_COMPLIED"
                            ? "badge bg-warning text-dark"
                            : result.status ===
                              "NEEDS_MANUAL_REVIEW"
                            ? "badge bg-info text-dark"
                            : result.status ===
                              "NOT_FOUND"
                            ? "badge bg-secondary"
                            : "badge bg-danger"
                        }
                      >
                        {result.status.replaceAll("_", " ")}
                      </span>

                    </td>

                    <td>

                      {(result.confidence * 100).toFixed(0)}%

                    </td>

                    <td>

                      {result.remarks}

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

export default EvaluationDetails;